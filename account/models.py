# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from cloudinary.models import CloudinaryField

from django.utils.translation import gettext_lazy as _
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255,blank=True, null=True)
    contract_no = models.CharField(max_length=255,blank=True, null=True)
    image = CloudinaryField('user_image',folder='user_image', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='user_account_groups',  # Custom reverse accessor for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_account_permissions',  # Custom reverse accessor for user_permissions
        blank=True
    )

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
