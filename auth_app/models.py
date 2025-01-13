from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['name', 'email']  

    def __str__(self):
        return self.name
