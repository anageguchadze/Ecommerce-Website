from rest_framework import serializers
from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')  # Show product name
    user_name = serializers.ReadOnlyField(source='user.name')  # Show user name

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'user_name', 'product', 'product_name', 'is_favorite', 'added_at']
