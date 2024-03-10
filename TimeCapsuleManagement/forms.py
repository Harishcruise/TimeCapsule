from django import forms
from django.forms import DateTimeInput
from .models import Capsule, CapsuleContent


class CapsuleForm(forms.ModelForm):
    VISIBILITY_CHOICES = [
        (False, 'Private'),  # The stored value is False for "Private"
        (True, 'Public'),  # The stored value is True for "Public"
    ]
    is_public = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-input', 'onfocus': 'adjustLabel(this.id)', 'onblur': 'resetLabel(this.id)'}
        ),
        initial=False
    )

    class Meta:
        model = Capsule
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6}),
            'unsealing_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-input'}
            ),
        }
