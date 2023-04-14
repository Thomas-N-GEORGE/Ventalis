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

    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="product_img/%Y/%m/%d/", blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    """This is our cart model."""

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def add_line_item(self, product, quantity):
        """
        Add a line item to the cart, update total price.
        Essentially accessed from product view.
        """
        
        li, created = LineItem.objects.get_or_create(product=product, cart=self)

        if not created:
            self.total_price -= li.price
            li.quantity += quantity         # Update line item quantity.   

        else:
            if quantity < 1000:             # Abort if quantity < 1000.
                li.delete()         
                return
            
            li.quantity = quantity
            
        li.save()
        self.total_price += li.price        # Update total cart price.

    def update_line_item(self, product, quantity):
        """
        Update a line item from cart, update total price.
        Essentially accessed from cart view.
        """

        if quantity < 1000:     # Abort if quantity < 1000.
            return
        
        li, created = LineItem.objects.update_or_create(product=product, cart=self)
        
        if not created:
            self.total_price -= li.price

        li.quantity = quantity
        li.save()
        self.total_price += li.price

    def remove_line_item(self, line_item):
        """Remove a line item from cart, update total price."""
    
        self.total_price -= line_item.price
        line_item.cart.delete()

    def empty_cart(self):
        """Remove all line items from cart, reset total price to 0."""

        li_set = LineItem.objects.filter(cart=self)
        for li in li_set:
            li.delete()

        self.total_price = 0


class LineItem(models.Model):
    """This is our line item model."""

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Model logic : 
        Quantity must be >= 1000, if not we update it to 1000, 
        we populate the price field when saving,
        (and the cart field as well ?)
        """

        if self.quantity < 1000:
            self.quantity = 1000

        self.price = self.product.price * self.quantity
        
        return super().save(*args, **kwargs)
