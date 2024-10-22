from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.conf import settings

class Property(models.Model):
    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        related_name='properties',
        null=True,
        blank=True
    )
    listing_type = models.CharField(max_length=4, choices=LISTING_TYPES, default='sale')
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bedrooms = models.IntegerField( null=True, blank=True)
    bathrooms = models.IntegerField( null=True, blank=True)
    square_meters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    property_type = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img.thumbnail((800, 800))  # Resize image
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            self.image = ContentFile(output.read(), name=self.image.name)
        super().save(*args, **kwargs)

    