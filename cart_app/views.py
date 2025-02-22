from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
import drf_yasg

# class CouponViewSet(ModelViewSet):
#     queryset = Coupon.objects.all()
#     serializer_class = CouponSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return super().get_queryset().filter(is_active=True)

#     def perform_create(self, serializer):
#         serializer.save()

        

# class CartItemViewSet(ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # Skip the permission check if we're generating schema with drf_yasg
#         if getattr(self, 'swagger_fake_view', False):
#             return self.queryset.all()

#         user = self.request.user
#         if not user.is_authenticated:
#             raise PermissionDenied("You must be logged in to view this data.")
#         return self.queryset.filter(cart=user)


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Skip the permission check if we're generating schema with drf_yasg
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.all()

        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view this data.")
        return self.queryset.filter(cart=user)

    def perform_create(self, serializer):
        """
        Override perform_create to set the cart field based on the
        user from the access token.
        """
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to perform this action.")
        
        serializer.save(cart=user)  # Set the cart field using the authenticated user

    def get_serializer(self, *args, **kwargs):
        """
        Override to only accept 'quantity' and 'product_id' fields in requests.
        """
        if self.action in ['create', 'update']:
            kwargs['data'] = kwargs.get('data', {}).copy()
            if 'cart' in kwargs['data']:
                kwargs['data'].pop('cart')  # Prevent users from manually setting the cart
        return super().get_serializer(*args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance.cart != request.user:
    #         return Response({"error": "You cannot delete this item"}, status=status.HTTP_403_FORBIDDEN)
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Skip the permission check if we're generating schema with drf_yasg
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.all()

        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view this data.")
        return self.queryset.filter(user=user)
    

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Skip the permission check if we're generating schema with drf_yasg
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.all()

        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view this data.")
        return self.queryset.filter(user=user)
