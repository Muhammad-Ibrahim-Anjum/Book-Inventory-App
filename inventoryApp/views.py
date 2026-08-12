from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import AuthorForm, BookForm
from .models import Author, Books

def home_view(request):
    books = Books.objects.all()
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
    
    books = Books.objects.select_related("author").prefetch_related("genres")
    return render(request, 'inventoryApp/book_list.html', {'books': books})

def book_detail_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    
    book = Books.objects.select_related("author").prefetch_related("genres").get(id=book_id)
    return render(request, 'inventoryApp/book_detail.html', {'book': book})


def book_update_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    if not request.user.is_staff:
        return redirect('inventoryApp:home')
    
    book = Books.objects.select_related("author").prefetch_related("genres").get(id=book_id)
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
    if not request.user.is_staff:
        return redirect('inventoryApp:home')
    
    book = Books.objects.select_related("author").prefetch_related("genres").get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('inventoryApp:book_list')
    
    return render(request, 'inventoryApp/book_confirm_delete.html', {'book': book})

def author_detail_view(request, author_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()  # Using the related_name defined in the ForeignKey
    return render(request, 'inventoryApp/author_detail.html', {'author': author, 'books': books})

def add_author_view(request):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    if not request.user.is_staff:
        return redirect('inventoryApp:home')

    form = AuthorForm()
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventoryApp:author_list')
    
    return render(request, 'inventoryApp/author_form.html', {'form': form})

def author_list_view(request):
    if not request.user.is_authenticated:
        return redirect('authApp:login')

    authors = Author.objects.all()
    return render(request, 'inventoryApp/authors_list.html', {'authors': authors})

def author_update_view(request, author_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    if not request.user.is_staff:
        return redirect('inventoryApp:home')

    author = get_object_or_404(Author, id=author_id)
    form = AuthorForm(instance=author)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('inventoryApp:author_list')
    
    return render(request, 'inventoryApp/author_form.html', {'form': form})

def author_delete_view(request, author_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')
    if not request.user.is_staff:
        return redirect('inventoryApp:home')

    author = Author.objects.get(id=author_id) 
    if request.method == 'POST':
        author.delete()
        return redirect('inventoryApp:author_list')
    
    return render(request, 'inventoryApp/book_confirm_author_delete.html', {'author': author})
