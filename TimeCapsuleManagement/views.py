from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Capsule, CapsuleContent, Comment, Subscription
from AuthenticationSystem.models import UserProfile
from .forms import CapsuleForm, CommentForm
import mimetypes
from django.http import HttpResponse
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
            # return redirect('TimeCapsuleManagement:my_capsules')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'success|{redirect_url}')
        else:
            messages.error(request, 'An error occurred while creating the capsule, please try again.')
            # return render(request, 'my_capsules.html', {'form': form})
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'error|{redirect_url}')
    else:
        form = CapsuleForm()
    return render(request, 'my_capsules.html', {'form': form, 'capsule_list': capsule_list,'comment_form': comment_form})


def delete_capsule(request, capsule_id):
    if request.method == "POST":  # Ensure the action is only allowed through POST request for safety
        capsule = get_object_or_404(Capsule, id=capsule_id)
        capsule.delete()
        messages.success(request, "Capsule deleted successfully!")
        return redirect('TimeCapsuleManagement:my_capsules')
    else:
        messages.error(request, "An error occurred, please try again.")
        return redirect('TimeCapsuleManagement:my_capsules')

def post_comment(request, capsule_id):
    capsule = Capsule.objects.get(pk=capsule_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.capsule = capsule
            comment.user = request.user  # Assuming user is logged in
            comment.save()
            return redirect('TimeCapsuleManagement:home')
    else:
        form = CommentForm()
        return redirect('TimeCapsuleManagement:home')