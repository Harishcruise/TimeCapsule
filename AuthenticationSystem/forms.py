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
        fields = ['username', 'email']

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'style': 'height: 50px;'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if user:
            # self.fields['username'].widget.attrs['readonly'] = True
            # self.fields['email'].widget.attrs['readonly'] = True
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def clean_username(self):
        return self.instance.username

    def clean_email(self):
        return self.instance.email