from rest_framework import viewsets
from .models import Category, SubCategory, Product
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """
        Add a review (rating) to a product.
        This will add a rating from 1 to 5 to the product's review field.
        """
        product = self.get_object()  # Get the product by ID
        user = request.user  # Get the currently authenticated user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to submit a review.")

        # Get rating from the request data
        rating = request.data.get('rating')

        # Validate the rating
        if not rating or not (1 <= rating <= 5):
            return Response({"error": "Rating must be between 1 and 5."}, status=400)

        # Set the review for the product (only one review per product)
        product.review = rating
        product.save()

        # Return a success response
        return Response({"message": "Review added successfully."})


#??