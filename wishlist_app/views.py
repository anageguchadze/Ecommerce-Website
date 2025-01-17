from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from cart_app.models import CartItem
from product_app.models import Product

class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Skip the permission check if we're generating schema with drf_yasg
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.all()  # Return all wishlist items (no user filter)

        # Regular permission check for authenticated users
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view this data.")
        return self.queryset.filter(user=user)

    def create(self, request, *args, **kwargs):
        # Add a product to the wishlist
        product_id = request.data.get("product")
        if not product_id:
            return Response({"detail": "Product ID is required"}, status=400)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"detail": "Product not found"}, status=404)

        # Check if the product is already in the wishlist
        if WishlistItem.objects.filter(user=request.user, product=product).exists():
            return Response({"detail": "Product already in wishlist"}, status=400)

        wishlist_item = WishlistItem.objects.create(user=request.user, product=product)
        return Response(WishlistItemSerializer(wishlist_item).data, status=201)

    def destroy(self, request, *args, **kwargs):
        # Remove a product from the wishlist
        wishlist_item = self.get_object()
        if wishlist_item.user != request.user:
            raise PermissionDenied("You cannot remove products from another user's wishlist.")
        wishlist_item.delete()
        return Response({"detail": "Product removed from wishlist"}, status=204)

    def add_all_to_cart(self, request):
        # Add all wishlist products to the user's cart
        user = request.user
        wishlist_items = WishlistItem.objects.filter(user=user)

        if not wishlist_items:
            return Response({"detail": "No products in wishlist"}, status=400)

        for item in wishlist_items:
            # Create cart item if it doesn't already exist
            CartItem.objects.get_or_create(cart=user, product=item.product, quantity=1)

        return Response({"detail": "All products added to cart"}, status=200)
