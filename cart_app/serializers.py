from rest_framework import serializers
from .models import Cart, CartItem, Coupon, Order


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'is_active', 'expires_at']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['product', 'product_name', 'quantity', 'total_price', 'product_price', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'is_active', 'created_at', 'coupon', 'items', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['user', 'cart', 'subtotal', 'shipping_fee', 'total_price', 'coupon_code', 
                  'first_name', 'company_name', 'street_address', 'apartment', 'city', 'phone_number', 
                  'email_address', 'created_at']
