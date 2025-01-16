from rest_framework import viewsets
from rest_framework.response import Response
from .models import Cart, CartItem, Coupon, Order
from .serializers import CartSerializer, CartItemSerializer, CouponSerializer, OrderSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = self.request.user.cart.filter(is_active=True).first()
        if cart:
            serializer.save(cart=cart)
        else:
            raise ValueError("Cart not found or is not active.")


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def apply_coupon(self, request, pk=None):
        cart = self.get_object()
        coupon_code = request.data.get('coupon_code', None)
        if coupon_code:
            try:
                cart.apply_coupon(coupon_code)
                return Response({'message': 'Coupon applied successfully'}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Coupon code is required'}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = self.request.user.cart.filter(is_active=True).first()
        if cart:
            # Calculate subtotal, shipping fee, and total price
            subtotal = sum(item.quantity * item.product.price for item in cart.items.all())
            shipping_fee = 0  # Assuming free shipping
            total_price = subtotal + shipping_fee
            serializer.save(
                cart=cart,
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                total_price=total_price
            )
        else:
            raise ValueError("Active cart not found.")
