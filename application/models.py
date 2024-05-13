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