from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # Ensure password is hashed
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """Creates and returns a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False, null=False)  # Ensure email cannot be blank
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255)  # This will still be used internally but stored as hashed password
    
    # Add these fields
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)  # Required for superuser privileges

    # Ensure the email is used as the primary identifier for the user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # email is already required for creating a user, so only name needs to be added

    # Using the custom user manager
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_lable):
        return True

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'custom_user'  # Ensures a unique table name for this custom user model



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"