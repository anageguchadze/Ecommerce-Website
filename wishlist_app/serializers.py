from rest_framework import serializers
from .models import WishlistItem
from product_app.models import Product

class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')  # Show product name

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'product_name', 'added_at']
