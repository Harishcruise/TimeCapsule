from django import forms
from django.forms import DateTimeInput
from .models import Capsule, CapsuleContent


class CapsuleForm(forms.ModelForm):
    class Meta:
        model = Capsule
        fields = '__all__'
        widgets = {
            'unsealing_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
