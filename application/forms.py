import re
from django import forms
from django.contrib.auth.models import User
from .models import User_detail

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    ic_number = forms.CharField(max_length=12, label='IC Number')
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")
        return username
    
    def clean_ic_number(self):
        ic_number = self.cleaned_data['ic_number']
        if not re.match(r'^\d{12}$', ic_number):
            raise forms.ValidationError("IC number must be exactly 12 digits.")
        return ic_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        ic_number = self.cleaned_data['ic_number']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        user_detail = User_detail.objects.create(user=user, ic_number=ic_number)
        return user, user_detail