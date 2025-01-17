from django.db import models
from auth_app.models import CustomUser
from product_app.models import Product


# class Coupon(models.Model):
#     code = models.CharField(max_length=20, unique=True)
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage off
#     is_active = models.BooleanField(default=True)  # Whether the coupon is active
#     expires_at = models.DateField()  

#     def __str__(self):
#         return self.code



class CartItem(models.Model):
    cart = models.ForeignKey(CustomUser, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()



class Order(models.Model):
    recipientName = models.CharField(max_length=255)
    recipientPhoneNumber = models.CharField(max_length=50)
    dateOfDelivery = models.DateField()
    deliveryTime = models.TimeField()
    street = models.CharField(max_length=255)
    houseNumber = models.CharField(max_length=10)
    total = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    quantity = models.FloatField()
