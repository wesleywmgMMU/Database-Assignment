from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect to a success page
                return redirect('home')
            else:
                # Return an error message or render the form with errors
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_homepage(request):
    user = request.user
    
    context = {
        'username': user.username,
    }

    return render(request, 'user_homepage.html', context)

@login_required
def admin_homepage(request):
    user = request.user
    
    context = {
        'username': user.username,
    }

    return render(request, 'admin_homepage.html', context)

@login_required
def home(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return redirect('admin_homepage')
    else:
        return redirect('user_homepage')
