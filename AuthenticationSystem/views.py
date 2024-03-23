import os
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomLoginForm, CustomSignupForm, EditProfileForm, CustomPasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from TimeCapsuleManagement.models import Capsule
from AuthenticationSystem.models import UserProfile, UserVisit
from TimeCapsuleManagement.forms import CommentForm
from AuthenticationSystem.crud_operations.auth_operations import create_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('TimeCapsuleManagement:home')

                # Calculate max_age for the cookie to expire at the end of the day
                now = timezone.now()
                end_of_day = timezone.datetime(now.year, now.month, now.day, 23, 59, 59,
                                               tzinfo=timezone.get_default_timezone())
                max_age = (end_of_day - now).total_seconds()

                new_visit_cookie_name = f'show_welcome_message_{user.username}'
                response.set_cookie(new_visit_cookie_name, 'true',
                                    max_age=int(max_age))  # Expires at the end of the day
                return response
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('AuthenticationSystem:user_login')
    else:
        form = CustomLoginForm()
    return render(request, 'user_login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('SearchCapsule:capsule_search')


def user_signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            create_user(username, password, email)
            messages.success(request, 'User created successfully')
            return redirect('AuthenticationSystem:user_login')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{error}")
    else:
        form = CustomSignupForm()
    return render(request, 'user_signup.html', {'form': form})


@login_required
def profile(request):
    update_user_history(request)
    if request.method == 'POST':
        owner = UserProfile.objects.get(id=request.user.id)
        # form = EditProfileForm(request.POST, instance=request.user)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, f'{owner} profile updated')
        #     return redirect('AuthenticationSystem:profile')

        if 'profile_submit' in request.POST:  # Check if profile form is submitted
            profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, f'{owner} profile updated')
                return redirect('AuthenticationSystem:profile')
        elif 'password_submit' in request.POST:  # Check if password form is submitted
            password_form = PasswordChangeForm(request.user, request.POST)
            print("hjje", password_form.is_valid())
            print(password_form.cleaned_data)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important for keeping the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('AuthenticationSystem:profile')
            else:
                print(password_form.errors)
                messages.success(request, f'Meet the requirements for password change {password_form.errors}')
                return redirect('AuthenticationSystem:profile')

    else:

        owner = UserProfile.objects.get(id=request.user.id)
        posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(owner=owner)
        users = UserProfile.objects.all()
        comment_form = CommentForm()
        password_form = PasswordChangeForm(request.user)
        form = EditProfileForm(instance=request.user)
        user_history_session = request.session.get('user_history', [])
        user_history_database = UserVisit.objects.filter(user=request.user).order_by('-timestamp')

        return render(request, 'profile.html',{'posts': posts, 'users': users, 'cur_user': owner, 'comment_form': comment_form, 'form': form, 'password_form': password_form, 'user_history': user_history_database[:15]})


@login_required
def update_user_history(request):
    if request.user.is_authenticated:
        # Store visit history in the session
        user_history = request.session.get('user_history', [])
        user_history.append({'page': request.path, 'timestamp': timezone.now().isoformat()})
        request.session['user_history'] = user_history
        UserVisit.objects.create(user=request.user, page=request.path)


@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get('profilepic'):
        user_profile = request.user
        old_profilepic_path = user_profile.profilepic.path if user_profile.profilepic else None
        # user_profile.profilepic.upload_to = f"static/images/{user_profile.id}/"
        user_profile.profilepic = request.FILES['profilepic']
        user_profile.save()
        if old_profilepic_path and os.path.exists(old_profilepic_path):
            os.remove(old_profilepic_path)
    return render(request, 'profile.html')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = '/accounts/password_reset/done/'
    form_class = CustomPasswordResetForm
