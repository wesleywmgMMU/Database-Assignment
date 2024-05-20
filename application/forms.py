import re
from django import forms
from django.contrib.auth.models import User
from .models import User_detail, Payment_method

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
    
class PaymentMethodForm(forms.ModelForm):
    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not re.match(r'^\d{16}$', card_number):
            raise forms.ValidationError("Card number must contain exactly 16 digits.")
        return card_number
    
    def clean_expiration_month(self):
        expiration_month = self.cleaned_data['expiration_month']
        if not expiration_month.isdigit():
            raise forms.ValidationError("Expiration month must contain only digits.")
        return expiration_month

    def clean_expiration_year(self):
        expiration_year = self.cleaned_data['expiration_year']
        if not expiration_year.isdigit():
            raise forms.ValidationError("Expiration year must contain only digits.")
        return expiration_year

    def clean_security_code(self):
        security_code = self.cleaned_data['security_code']
        if not security_code.isdigit():
            raise forms.ValidationError("Security code must contain only digits.")
        return security_code
    
    def save(self, user=None, commit=True):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Payment_method
        fields = ['cardholder_name', 'card_number', 'expiration_month', 'expiration_year', 'security_code', 'billing_address']