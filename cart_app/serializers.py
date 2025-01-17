from rest_framework import serializers
from .models import  CartItem, Order, OrderItem


# class CouponSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Coupon
#         fields = ['code', 'discount_percentage', 'is_active', 'expires_at']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', None)
        super().__init__(*args, **kwargs)
        

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')  # Show product name

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Include related order items

    class Meta:
        model = Order
        fields = '__all__'
    