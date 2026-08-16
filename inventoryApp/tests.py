import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Author, Books, Genre


@pytest.mark.django_db
def test_book_list_is_not_n_plus_one(client, django_assert_num_queries):
    user = get_user_model().objects.create_user(username="tester", password="pass123")
    author = Author.objects.create(name="Test Author", nationality="Test")
    genre = Genre.objects.create(name="Fantasy")
    book = Books.objects.create(title="Test Book", author=author, available_copies=1)
    book.genres.add(genre)

    client.force_login(user)

    with django_assert_num_queries(4):
        client.get(reverse("inventoryApp:book_list"))
