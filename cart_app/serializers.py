from rest_framework import serializers
from .models import Cart, CartItem
from product_app.serializers import ProductSerializer 

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    coupon = serializers.CharField(allow_blank=True, required=False)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['user', 'is_active', 'created_at', 'items', 'coupon', 'total_price']
