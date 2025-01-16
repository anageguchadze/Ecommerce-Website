from django.db import models
from auth_app.models import CustomUser
from product_app.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)  # Mark product as favorite

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"

    class Meta:
        db_table = 'wishlist'
        unique_together = ('user', 'product')  # Prevent duplicate entries
        ordering = ['-added_at']
