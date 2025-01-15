from django.db import models
from product_app.models import Product

class Sale(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Many-to-many relationship with products
    products = models.ManyToManyField(Product, related_name='sales')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sale'

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    ]
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    applicable_categories = models.ManyToManyField('product_app.Category', related_name='discounts', blank=True)
    applicable_products = models.ManyToManyField(Product, related_name='discounts', blank=True)

    def __str__(self):
        return f"{self.discount_value} {self.discount_type}"

    class Meta:
        db_table = 'discount'


