from django.shortcuts import render, redirect

# Create your views here.
from .forms import BookForm
from .models import Book

def home_view(request):
    books = Book.objects.all()
    return render(request, 'inventoryApp/home.html', {'books': books})

def add_book_view(request):
    form = BookForm()
    user = request.user
    if not user.is_staff:
        return redirect('inventoryApp:home')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventoryApp:book_list')
        
    return render(request, 'inventoryApp/book_form.html', {'form': form})

def book_list_view(request):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    
    books = Book.objects.all()
    return render(request, 'inventoryApp/book_list.html', {'books': books})


def book_update_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    
    book = Book.objects.get(book_id=book_id)
    form = BookForm(instance=book)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('inventoryApp:book_list')
        
    return render(request, 'inventoryApp/book_form.html', {'form': form})

def book_delete_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('inventoryApp:book_list')
    
    return render(request, 'inventoryApp/book_confirm_delete.html', {'book': book})