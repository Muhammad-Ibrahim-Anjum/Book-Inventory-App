from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'book_id': 'Book ID',
            'sku': 'SKU',
            'title': 'Title',
            'author': 'Author',
            'description': 'Description',
            'price': 'Price',
            'quantity': 'Quantity',
            'published_date': 'Published Date',
        }
        widgets = {
            'book_id': forms.NumberInput(attrs={'placeholder': 'Book ID', 'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'placeholder': 'SKU', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantity', 'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'placeholder': 'Published Date', 'class': 'form-control', 'type': 'date'}),
        }