from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add/', views.add_book_view, name='add_book'),
    path('list/', views.book_list_view, name='book_list'),
    path('update/<int:book_id>/', views.book_update_view, name='book_update'),
    path('delete/<int:book_id>/', views.book_delete_view, name='book_delete'),
]