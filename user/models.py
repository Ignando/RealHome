from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from PIL import Image
import io
from django.core.files.base import ContentFile
# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    user_type = models.CharField(max_length=10, choices=[('customer', 'Customer'), ('realtor', 'Realtor')])
    license_number = models.CharField(max_length=50, blank=True, null=True)

    # Add these lines to resolve the clash:
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username