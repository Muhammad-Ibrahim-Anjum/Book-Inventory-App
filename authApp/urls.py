from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_form, name='login'),
    path('register/', views.register_form, name='register'),
    path('logout/', views.logout_form, name='logout'),
]