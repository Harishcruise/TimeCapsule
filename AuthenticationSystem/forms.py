from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CustomSignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'style': 'height: 50px;'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio', 'first_name', 'last_name']