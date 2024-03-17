from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Capsule, CapsuleContent, Comment, Subscription
from AuthenticationSystem.models import UserProfile
from .forms import CapsuleForm, CommentForm
import mimetypes
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def home(request):
    posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').all()
    users = UserProfile.objects.all()
    comment_form = CommentForm()
    return render(request, 'home.html', {'posts': posts, 'users': users, 'comment_form': comment_form})


@login_required
def my_capsules(request):
    comment_form = CommentForm()
    owner = UserProfile.objects.get(id=request.user.id)
    capsule_list = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(owner=owner)
    if request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user.id
        form = CapsuleForm(data, request.FILES)
        if form.is_valid():
            capsule = form.save()

            # Handle the uploaded files for CapsuleContent
            files = request.FILES.getlist('capsule_contents')
            for file in files:
                mime_type, _ = mimetypes.guess_type(file.name)
                file_type = 'text'  # Default file type
                if mime_type:
                    if mime_type.startswith('image/'):
                        file_type = 'photo'
                    elif mime_type.startswith('video/'):
                        file_type = 'video'
                # Create a CapsuleContent object for each file
                CapsuleContent.objects.create(
                    file=file,
                    capsule=capsule,
                    file_type=file_type,  # Use the determined file type
                )
            messages.success(request, 'Time Capsule created successfully!')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'success|{redirect_url}')
        else:
            messages.error(request, 'An error occurred while creating the capsule, please try again.')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'error|{redirect_url}')
    else:
        form = CapsuleForm()
    return render(request, 'my_capsules.html', {'form': form, 'capsule_list': capsule_list,'comment_form': comment_form})


@login_required
def edit_capsule(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id, owner=request.user)

    if request.method == 'GET':
        data = {
            'name': capsule.name,
            'description': capsule.description,
            'unsealing_date': capsule.unsealing_date.strftime('%Y-%m-%dT%H:%M'),
            'is_public': capsule.is_public,
            'status': capsule.status,
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user.id
        form = CapsuleForm(data, request.FILES, instance=capsule)
        if form.is_valid():
            updated_capsule = form.save()
            contents_to_delete = request.POST.getlist('filesToDelete', [])
            CapsuleContent.objects.filter(id__in=contents_to_delete).delete()
            files = request.FILES.getlist('capsule_contents')
            for file in files:
                mime_type, _ = mimetypes.guess_type(file.name)
                file_type = 'photo'  # Default file type
                if mime_type:
                    if mime_type.startswith('image/'):
                        file_type = 'photo'
                    elif mime_type.startswith('video/'):
                        file_type = 'video'
                CapsuleContent.objects.create(
                    file=file,
                    capsule=updated_capsule,
                    file_type=file_type
                )

            messages.success(request, 'Capsule updated successfully!')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'success|{redirect_url}')
        else:
            messages.error(request, 'An error occurred while updating the capsule.')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'error|{redirect_url}')


@login_required
def get_capsule_contents(request, capsule_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            contents = CapsuleContent.objects.filter(capsule_id=capsule_id).values('id', 'file', 'file_type')
            return JsonResponse(list(contents), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_capsule(request, capsule_id):
    if request.method == "POST":
        capsule = get_object_or_404(Capsule, id=capsule_id)
        capsule.delete()
        messages.success(request, "Capsule deleted successfully!")
        return redirect('TimeCapsuleManagement:my_capsules')
    else:
        messages.error(request, "An error occurred, please try again.")
        return redirect('TimeCapsuleManagement:my_capsules')


@login_required
def post_comment(request, capsule_id):
    capsule = Capsule.objects.get(pk=capsule_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.capsule = capsule
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment saved successfully!")
            # return redirect('TimeCapsuleManagement:home')
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
    else:
        form = CommentForm()
        # return redirect('TimeCapsuleManagement:home')
        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer_url)
