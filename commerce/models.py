from django.db import models
from decimal import Decimal
from django.contrib.postgres.fields import JSONField


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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/products/')
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)
    stock = models.BooleanField(default=False)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    model = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    @property
    def get_absolute_url(self):
        return self.image.url

    @property
    def discounted_price(self):
        if self.discount > 0:
            self.price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        return Decimal(self.price).quantize(Decimal('0.001'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Order(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    @property
    def subtotal_price(self):
        order_items = self.orderitem_set.all()
        subtotal = sum(item.product.price * item.quantity for item in order_items if item.product)
        return Decimal(subtotal).quantize(Decimal('0.001'))

    @property
    def tax_price(self):
        tax = (self.subtotal_price / 100) * 5
        return Decimal(tax).quantize(Decimal('0.001'))

    @property
    def total_price(self):
        return self.subtotal_price + self.tax_price

    def __str__(self):
        return self.name


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} => {self.order}'