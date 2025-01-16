from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem, Coupon
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.exceptions import ValidationError

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    # Additional action to apply coupon
    @action(detail=True, methods=['post'], url_path='apply-coupon')
    def apply_coupon(self, request, pk=None):
        # Get cart object
        cart = self.get_object()

        # Get coupon code from request
        coupon_code = request.data.get('coupon_code', None)

        if not coupon_code:
            raise ValidationError("Coupon code is required.")

        try:
            # Attempt to apply coupon to the cart
            cart.apply_coupon(coupon_code)
            # Return the updated cart with new total price
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            # Coupon application failed, return error
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # You may also override the update method to auto-calculate the total price
    def perform_update(self, serializer):
        cart = serializer.save()
        cart.update_total_price()  # Recalculate total when cart is updated

    @action(detail=True, methods=['get'], url_path='total')
    def get_total(self, request, pk=None):
        cart = self.get_object()
        return Response({"total_price": cart.total_price}, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    # Optionally, we can add custom actions for CartItem if necessary
    def perform_create(self, serializer):
        # Make sure total price is updated after item is added
        cart_item = serializer.save()
        cart_item.cart.update_total_price()

    def perform_update(self, serializer):
        # Make sure total price is updated after item quantity is changed
        cart_item = serializer.save()
        cart_item.cart.update_total_price()

    def perform_destroy(self, instance):
        # Remove item from cart and update the total price
        cart = instance.cart
        instance.delete()
        cart.update_total_price()
