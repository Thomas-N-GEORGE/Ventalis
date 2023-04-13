from django.db import models

from django.utils import timezone

# Create your models here.

class Category(models.Model):
    """This is our Category model, to group Products."""

    name = models.CharField(max_length=200, unique=True)     # The default form widget for this field is a TextInput.

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """This is our Product model."""

    name = models.CharField(max_length=200, unique=True)     # The default form widget for this field is a TextInput.
    date_created = models.DateTimeField(default=timezone.now)     # The default form widget for this field is a single DateTimeInput.
    image = models.ImageField(upload_to="product_img/%Y/%m/%d/", blank=True, null=True)    # The default form widget for this field is a ClearableFileInput
    description = models.TextField()    # The default form widget for this field is a Textarea.
    price = models.DecimalField(max_digits=10, decimal_places=2)   # The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
