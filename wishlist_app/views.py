from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the logged-in user's wishlist
        return Wishlist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product')

        # Check if product is already in wishlist
        if Wishlist.objects.filter(user=user, product_id=product_id).exists():
            return Response({'detail': 'Product already in wishlist'}, status=status.HTTP_400_BAD_REQUEST)

        # Add product to wishlist
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        # Update `is_favorite` for a specific wishlist item
        instance = self.get_object()
        instance.is_favorite = request.data.get('is_favorite', instance.is_favorite)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Allow users to remove a product from their wishlist
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Product removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)
