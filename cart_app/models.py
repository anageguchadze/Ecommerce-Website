from django.db import models
from auth_app.models import CustomUser
from product_app.models import Product


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage off
    is_active = models.BooleanField(default=True)  # Whether the coupon is active
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    is_active = models.BooleanField(default=True)  # To manage active vs. completed carts
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)  # Optional coupon field
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Store the total price

    def __str__(self):
        return f"Cart of {self.user.name}"

    def apply_coupon(self, coupon_code):
        try:
            # Fetch the coupon based on the code
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            self.coupon = coupon
            self.save()  # Save the cart with the applied coupon
            self.update_total_price()  # Update the cart total after applying the coupon
        except Coupon.DoesNotExist:
            raise ValueError("Invalid coupon code")

    def update_total_price(self):
        # Calculate the total price based on Cart Items
        total = sum(item.quantity * item.product.price for item in self.items.all())  # Calculate total without discount

        if self.coupon:  # Apply discount if coupon exists
            discount = (self.coupon.discount_percentage / 100) * total
            total -= discount
        
        self.total_price = total
        self.save()  # Save the updated cart total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.name}'s cart"

    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-added_at']
