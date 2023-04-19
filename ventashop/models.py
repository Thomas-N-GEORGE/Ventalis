from django.db import models

from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.utils import timezone

from .utils import unique_ref_number_generator

# Create your models here.

class Category(models.Model):
    """This is our Category model, aimed to group and filter Products."""

    name = models.CharField(max_length=200, unique=True)     # The default form widget for this field is a TextInput.
    slug = models.SlugField(null=False, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    """This is our Product model."""

    class Meta:
        ordering = ["-date_created"]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=False, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="product_img/%Y/%m/%d/", blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Cart(models.Model):
    """This is our cart model."""

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Where should we put this relation ? Here or in CustomerAccount model class ??
    # owner = models.OneToOne(CustomerAccount)

    def calculate_total_price(self):
        """A utility method to summ up the prices of all the line items in cart."""

        self.total_price = 0

        for li in LineItem.objects.filter(cart=self):
            self.total_price += li.price


    def add_line_item(self, product, quantity):
        """
        Add a line item to the cart, update total price.
        Essentially accessed from product view.
        """
        
        li, created = LineItem.objects.get_or_create(product=product, cart=self)

        if not created:
            li.quantity += quantity         # Update line item quantity.   
        else:
            if quantity < 1000:             # Abort if quantity < 1000.
                li.delete()         
                return
            
            li.quantity = quantity
            
        li.save()
        self.save()

    def update_line_item(self, product, quantity):
        """
        Update a line item from cart, update total price.
        Essentially accessed from cart view.
        """

        if quantity < 1000:     # Abort if quantity < 1000.
            return
        
        li, created = LineItem.objects.update_or_create(product=product, cart=self)
        
        li.quantity = quantity
        li.save()
        self.save()

    def remove_line_item(self, line_item):
        """Remove a line item from cart, update total price."""
    
        line_item.delete()
        self.save()

    def empty_cart(self):
        """Remove all line items from cart, reset total price to 0."""

        for li in self.lineitem_set.all():
            li.delete()

        self.save()

    def make_order(self): 
        """
        Make order with line items of cart.
        We do not delete the line items, 
        rather we create a new Order object, 
        link the line items to it and then unlink them from the cart.

        returns : order[Order]
        """

        if self.total_price == 0:   # abort if cart is empty
            return
        
        order = Order.objects.create()
        order.add_comment()
        # order.owner = self.owner

        for li in self.lineitem_set.all():
            li.order = order
            li.cart = None
            li.save()

        order.save()
        self.save()

        return order

    def save(self, *args, **kwargs):
        """
        We calculate the total price to populate / update the field.
        """

        self.calculate_total_price()
        
        return super().save(*args, **kwargs)
        

class Order(models.Model):
    """This is our order model."""

    class Meta:
        ordering = ["-date_created"]
        

    # Choices for the state :
    NON_TRAITEE = "NT"
    EN_COURS_DE_TRAITEMENT = "CT"
    EN_ATTENTE_APPROVISIONNEMENT = "AA"
    PREPARATION_EXPEDITION = "PE"
    EN_ATTENTE_PAIEMENT ="AP"
    EXPEDIEE = "EX"
    TRAITEE_ARCHIVEE = "TA"
    ANNULEE = "AN"

    STATUS_CHOICES = [
        (NON_TRAITEE, "Non traitée"),
        (EN_COURS_DE_TRAITEMENT, "En cours de traitement"),
        (EN_ATTENTE_APPROVISIONNEMENT, "En attente d'approvisionnement"),
        (PREPARATION_EXPEDITION, "En préparation à l'expédition"),
        (EN_ATTENTE_PAIEMENT, "En attente de paiement"),
        (EXPEDIEE, "Expédiée"),
        (TRAITEE_ARCHIVEE, "Traitée"),
        (ANNULEE, "Annulée"),
    ]

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=NON_TRAITEE,)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=timezone.now)
    ref_number = models.CharField(max_length=20, blank= True)   # generated in self.save() method.
    slug = models.SlugField(null=False, unique=True)
    # owner = models.Foreignkey(CustomerAccount)

    def __str__(self):
        return self.ref_number
    
    def calculate_total_price(self):
        """A utility method to summ up the prices of all the line items in order."""

        self.total_price = 0

        for li in LineItem.objects.filter(order=self):
            self.total_price += li.price

    def add_comment(self, content="La commande vient d'être créée."):
        """Add a new comment to order."""

        comment = Comment.objects.create(content=content, order = self)
        comment.save()

    def save(self, *args, **kwargs):
        """
        We generate a random ref_number to populate the field.
        And we calculate the total price to populate the field.
        """

        if not self.ref_number:
            self.ref_number= unique_ref_number_generator(self)

        if not self.slug:
            self.slug = slugify(self.ref_number)

        self.calculate_total_price()
        
        return super().save(*args, **kwargs)


class Comment(models.Model):
    """This is our comment model, related to order model."""

    class Meta:
        ordering = ["-date_created"]


    content = models.CharField(max_length=2000, null=False)
    date_created = models.DateTimeField(default=timezone.now)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    

class LineItem(models.Model):
    """This is our line item model."""

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

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
