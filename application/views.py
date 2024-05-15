from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, PaymentMethodForm
from .models import Payment_method
from django.http import HttpResponse

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
    user_has_payment_method = Payment_method.objects.filter(user=user).exists()

    if user_has_payment_method:
        payment_methods = Payment_method.objects.using('read_masked_data').filter(user=user)
    else:
        return redirect('add_payment_method')
    
    context = {
        'username': user.username,
        'user_has_payment_method': user_has_payment_method,
        'payment_methods': payment_methods,
    }

    return render(request, 'user_homepage.html', context)

@login_required
def add_payment_method(request):
    user = request.user
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('home')
    else:
        form = PaymentMethodForm()
    
    context = {
        'username': user.username,
        'form': form,
    }

    return render(request, 'add_payment_method.html', context)

@login_required
def edit_payment_method(request, payment_method_id):
    user = request.user
    payment_method = Payment_method.objects.get(pk=payment_method_id)

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            return redirect('home') 
        
        form = PaymentMethodForm(instance=payment_method)

    context = {
        'username': user.username,
        'form': form,
    }

    return render(request, 'edit_payment_method.html', context)

@login_required
def remove_payment_method(request, payment_method_id):
    if request.method == 'POST':
        payment_method = Payment_method.objects.get(pk=payment_method_id)
        payment_method.delete()
        return redirect('home')  
    else:
        return HttpResponse("Method not allowed", status=405)

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
