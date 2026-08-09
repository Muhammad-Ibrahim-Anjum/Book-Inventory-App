from django import forms
from .models import Author, Books

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        # Keep explicit fields that exist on the Books model
        fields = ['title', 'description', 'published_date', 'author', 'genres', 'available_copies']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'published_date': 'Published Date',
            'author': 'Author',
            'genres': 'Genres',
            'available_copies': 'Available Copies',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control', 'maxlength': 100}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 4}),
            'published_date': forms.DateInput(attrs={'placeholder': 'Published Date', 'class': 'form-control', 'type': 'date'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'placeholder': 'Available Copies', 'class': 'form-control', 'min': 0}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_year', 'nationality']

        labels = {
            'name': 'Name',
            'bio': 'Biography',
            'birth_year': 'Birth Year',
            'nationality': 'Nationality',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control', 'maxlength': 200}),
            'bio': forms.Textarea(attrs={'placeholder': 'Biography', 'class': 'form-control', 'rows': 4}),
            'birth_year': forms.NumberInput(attrs={'placeholder': 'Birth Year', 'class': 'form-control', 'min': 0}),
            'nationality': forms.TextInput(attrs={'placeholder': 'Nationality', 'class': 'form-control', 'maxlength': 100}),
        }