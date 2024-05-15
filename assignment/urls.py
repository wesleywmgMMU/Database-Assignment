"""
URL configuration for assignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from application import views

urlpatterns = [
    path('db/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('user/', views.user_homepage, name='user_homepage'),
    path('user/add/', views.add_payment_method, name='add_payment_method'),
    path('user/edit/<int:payment_method_id>/', views.edit_payment_method, name='edit_payment_method'),
    path('user/remove/<int:payment_method_id>/', views.remove_payment_method, name='remove_payment_method'),
    path('admin/', views.admin_homepage, name='admin_homepage'),
    path('', views.home, name='home'),
]
