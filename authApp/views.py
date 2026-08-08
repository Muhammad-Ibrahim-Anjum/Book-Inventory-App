from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm


# Create your views here.
def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('inventoryApp:home')
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    return render(request, 'accounts/register.html', {'form': form})

def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'inventoryApp:home'
            return redirect(next_url)
        else:
            error_message = "Invalid username or password"
            return render(request, 'accounts/login.html', {
                'error_message': error_message,
                'next': request.POST.get('next', ''),
            })
    else:
        return render(request, 'accounts/login.html', {
            'next': request.GET.get('next', ''),
        })
    
def logout_form(request):
    if request.method == 'POST':
        logout(request)
        return redirect('authApp:login')
    else:
        return render(request, 'accounts/logout.html')
    
@login_required
def home_view(request):
    return render(request, 'auth_app/home.html')
