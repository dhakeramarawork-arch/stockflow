from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories."""
    class Meta:
        model = Category
        fields = ['name', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Electronics',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Short description of the category...',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }