from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Capsule, CapsuleContent, Comment, Subscription
from AuthenticationSystem.models import UserProfile
from .forms import CapsuleForm
import mimetypes


# Create your views here.


def home(request):
    return render(request, 'home.html')


def my_capsules(request):
    if request.method == 'POST':
        form = CapsuleForm(request.POST, request.FILES)
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
            return redirect('TimeCapsuleManagement:my_capsules')
    else:
        form = CapsuleForm()
    return render(request, 'my_capsules.html', {'form': form})
