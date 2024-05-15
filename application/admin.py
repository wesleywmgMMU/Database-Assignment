from django.contrib import admin
from .models import User_detail, Payment_method

# Register your models here.
admin.site.register(User_detail)
admin.site.register(Payment_method)
