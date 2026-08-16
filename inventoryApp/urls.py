from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add/', views.add_book_view, name='add_book'),
    path('list/', views.book_list_view, name='book_list'),
    path('update/<int:book_id>/', views.book_update_view, name='book_update'),
    path('delete/<int:book_id>/', views.book_delete_view, name='book_delete'),
    path('detail/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('author/add/', views.add_author_view, name='add_author'),
    path('author/list/', views.author_list_view, name='author_list'),
    path('author/detail/<int:author_id>/', views.author_detail_view, name='author_detail'),
    path('author/update/<int:author_id>/', views.author_update_view, name='author_update'), 
    path('author/delete/<int:author_id>/', views.author_delete_view, name='author_delete'),
    path('borrow/<int:book_id>/', views.borrow_book_view, name='borrow_book'),
    path('borrowed/', views.borrowed_books_view, name='borrowed_books'),
    path('unborrow/<int:book_id>/', views.unborrow_book_view, name='unborrow_book'),
    path('become-member/', views.become_member_view, name='become_member'),
]