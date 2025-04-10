import uuid
import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
phone_number_validator = RegexValidator(
    regex=r'^\d{11}$',
    message=_("Phone number must be exactly 11 digits long."),
)


class CustomUserManager(BaseUserManager):
    """Custom user manager for CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # inherited from AbstractBaseUser and hashes the password the password
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        """create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email as the username field."""
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    full_name = models.CharField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_number_validator],
        null=False,
        blank=True
    )
    country = models.CharField(max_length=50, default="Nigeria")
    state = models.CharField(max_length=50, default="Lagos")
    password = models.CharField(max_length=128, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # use email instead of username
    REQUIRED_FIELDS = ["full_name", "phone_number"]  # required fields for createsuperuser

    def __str__(self):
        return f"{self.email}: {self.full_name}"
    
    class meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]