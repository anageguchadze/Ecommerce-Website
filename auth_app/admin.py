from django.contrib import admin
from .models import CustomUser, Address
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Address)