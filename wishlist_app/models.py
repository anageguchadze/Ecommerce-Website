from django.db import models
from auth_app.models import CustomUser
from product_app.models import Product

class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, related_name="wishlist", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - Wishlist'
