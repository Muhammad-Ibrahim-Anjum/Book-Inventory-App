from django.shortcuts import render, redirect, get_object_or_404

from inventoryApp.python_logics import generate_membership_number

# Create your views here.
from .forms import AuthorForm, BookForm
from .models import Author, Books, Member

# Book Views

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
    borrowed_ids = set()
    if hasattr(request.user, "member"):
        borrowed_ids = set(
            request.user.member.borrow_records.values_list("book_id", flat=True)
        )

    return render(request, 'inventoryApp/book_list.html', {
        'books': books,
        'borrowed_ids': borrowed_ids,
    })

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

# Author Views

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
    
    return render(request, 'inventoryApp/author_confirm_delete.html', {'author': author})

# Memebership Views

def become_member_view(request):
    if not request.user.is_authenticated:
        return redirect('authApp:login')

    if hasattr(request.user, 'member'):
        return redirect('inventoryApp:home')  # Already a member

    if request.method == 'POST':
        number = generate_membership_number()
        Member.objects.create(
            user=request.user,
            membership_number=number,
        )
        return redirect('inventoryApp:home')

    return render(request, 'inventoryApp/become_member.html')

# Borrowing Views

def borrow_book_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')

    book = get_object_or_404(Books, id=book_id)
    member = request.user.member

    if book.available_copies > 0:
        # Create a borrow record
        from datetime import date, timedelta
        borrowed_on = date.today()
        due_date = borrowed_on + timedelta(days=14)  # 2 weeks borrowing period
        member.borrow_records.create(book=book, borrowed_on=borrowed_on, due_date=due_date)

        # Decrease the available copies of the book
        book.available_copies -= 1
        book.save()

        return redirect('inventoryApp:borrowed_books')
    else:
        return render(request, 'inventoryApp/book_unavailable.html', {'book': book})

def borrowed_books_view(request):
    if not request.user.is_authenticated:
        return redirect('authApp:login')

    borrowed_records = request.user.member.borrow_records.select_related("book").all()
    return render(request, 'inventoryApp/borrowed_books.html', {'borrowed_records': borrowed_records})

def unborrow_book_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('authApp:login')

    book = get_object_or_404(Books, id=book_id)
    member = request.user.member

    # Find the borrow record for this book and member
    borrow_record = member.borrow_records.filter(book=book).first()

    if borrow_record:
        # Increase the available copies of the book
        book.available_copies += 1
        book.save()

        # Delete the borrow record
        borrow_record.delete()

    return redirect('inventoryApp:borrowed_books')