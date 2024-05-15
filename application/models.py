from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class User_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ic_number = models.CharField(max_length=12, unique=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Detail"

    def __str__(self):
        return self.user.username
    
class Payment_method(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=100, blank=False)
    card_number = models.CharField(max_length=16, blank=False)
    expiration_month = models.CharField(max_length=2, blank=False)
    expiration_year = models.CharField(max_length=2, blank=False)
    security_code = models.CharField(max_length=4, blank=False)
    billing_address = models.CharField(max_length=255, blank=False)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Method"

    def __str__(self):
        return self.cardholder_name