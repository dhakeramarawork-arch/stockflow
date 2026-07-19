from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Product create/edit form. SKU auto-generated on create."""
    class Meta:
        model = Product
        fields = [
            'name', 'barcode', 'category', 'brand', 'unit', 'supplier',
            'purchase_price', 'selling_price', 'tax',
            'current_stock', 'minimum_stock', 'maximum_stock',
            'image', 'description', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barcode (optional)'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'minimum_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'maximum_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_selling_price(self):
        selling = self.cleaned_data.get('selling_price')
        purchase = self.cleaned_data.get('purchase_price')
        if selling is not None and purchase is not None and selling < purchase:
            raise forms.ValidationError('Selling price cannot be less than purchase price.')
        return selling

    def clean(self):
        cleaned = super().clean()
        minimum = cleaned.get('minimum_stock')
        maximum = cleaned.get('maximum_stock')
        if minimum is not None and maximum is not None and minimum > maximum:
            raise forms.ValidationError('Minimum stock cannot exceed maximum stock.')
        return cleaned