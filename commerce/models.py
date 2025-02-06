import random
import string
import uuid
from django.db import models
from decimal import Decimal
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5


    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE.value)
    # image = models.ImageField(upload_to='media/products/', null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    stock = models.CharField(max_length=20, default="Not Available")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    model = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return (self.price * (Decimal(1) - Decimal(self.discount) / 100)).quantize(Decimal('0.01'))
        return self.price

    def is_new(self):
        return (now() - self.created_at).total_seconds() < 86400

    def save(self, *args, **kwargs):
        self.stock = "Available" if self.quantity > 0 else "Sold Out"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='media/products/')

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"



class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,related_name='product_attributes', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, blank=True)


class Order(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=20, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    billing_address = models.TextField(default="No Billing Address")
    shipping_address = models.TextField(default="No Shipping Address")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_totals(self):
        self.subtotal = sum(
            item.quantity * item.product.discounted_price for item in self.order_items.all()
        )
        self.tax = (self.subtotal * Decimal(0.05)).quantize(Decimal('0.01'))
        self.total = self.subtotal + self.tax
        self.save()

    def __str__(self):
        return f"Order #{self.order_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Comment(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments',
                                null=True, blank=True)
    is_negative = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} => {self.created_at}'

    class Meta:
        # verbose_name = 'comment'
        ordering = ['-created_at']

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def generate_invoice_prefix():
    return ''.join(random.choices(string.ascii_uppercase, k=5))


class Customer(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True, default="No Description")
    vat_number = models.CharField(max_length=50, blank=True, null=True, default="No VAT number")

    send_email_to = models.EmailField()
    address = models.TextField()
    phone_number = PhoneNumberField(region="UZ")
    invoice_prefix = models.CharField(max_length=5, default=generate_invoice_prefix, unique=True)
    invoice_number = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.invoice_prefix:
            self.invoice_prefix = generate_invoice_prefix()

        if not self.invoice_number:
            self.invoice_number = 1

        super().save(*args, **kwargs)

    def generate_invoice_id(self):
        return f"{self.invoice_prefix}-{self.invoice_number:05d}"

    def __str__(self):
        return f'{self.full_name} -> {self.generate_invoice_id()}'


class Favourite(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"