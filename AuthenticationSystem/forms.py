from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CustomSignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}), required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check for minimum password length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Check for password complexity (example: requiring at least one digit)
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")

        # At least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # At least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Return the cleaned data
        return password


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio', 'first_name', 'last_name']