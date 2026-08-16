from django.conf import settings
from django.db import models
 
 
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=100)
 
    def __str__(self):
        return self.name
 
 
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
 
    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",       # lets you do author.books.all()
    )
    genres = models.ManyToManyField(Genre, related_name="books", blank=True)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'inventoryApp_books'


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership_number = models.CharField(max_length=20, unique=True)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return f"{self.membership_number} ({self.user.username})"
 
 
class BorrowRecord(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="borrow_records")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="borrow_records")
    borrowed_on = models.DateField()
    due_date = models.DateField()
    returned_on = models.DateField(null=True, blank=True)   # None = still borrowed
 
    def __str__(self):
        return f"{self.book.title} → {self.member.membership_number}"