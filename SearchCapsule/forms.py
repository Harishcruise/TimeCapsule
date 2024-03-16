# forms.py
from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search...',
            'class': 'search-input',
            'aria-label': 'Search'
        })
    )
