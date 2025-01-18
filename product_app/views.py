from rest_framework import viewsets
from .models import Category, SubCategory, Product, ImageSlider, ProductRating
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ImageSliderSerializer, ProductRatingSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
    
    filter_backends = [SearchFilter]  # Enable search filter
    search_fields = ['name']  


class NewArrivalsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Get the current date and time
        now = timezone.now()
        
        # Filter products created within the last 30 days
        thirty_days_ago = now - timedelta(days=30)
        return Product.objects.filter(created_at__gte=thirty_days_ago, is_active=True).order_by('-created_at')  # Order by latest first
    

class BestSellersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Fetch all products
        products = Product.objects.all()
        
        # Handle case where there are fewer than 10 products
        sample_size = min(len(products), 10)  # Ensure we don't sample more than the available products
        random_products = random.sample(list(products), k=sample_size)  # Randomly select products
        
        # Serialize the selected products
        serializer = ProductSerializer(random_products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ImageSliderListView(generics.ListAPIView):
    queryset = ImageSlider.objects.all()  # Retrieve all image sliders
    serializer_class = ImageSliderSerializer
    permission_classes = [AllowAny]


class ProductRatingView(APIView):
    permission_classes = [AllowAny]  # Allow everyone to access this endpoint

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        session_id = request.COOKIES.get('sessionid')  # Retrieve session ID for guests
        user = request.user if request.user.is_authenticated else None

        if not user and not session_id:
            return Response({"error": "Unable to identify guest. Ensure cookies are enabled."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user/session has already rated
        existing_rating = ProductRating.objects.filter(
            product=product,
            user=user if user else None,
            session_id=session_id if not user else None
        ).first()

        if existing_rating:
            return Response({"error": "You have already rated this product"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and save the rating
        serializer = ProductRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=user, 
            session_id=session_id if not user else None,
            product=product
        )

        # Update the average rating of the product
        product.update_average_rating()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        ratings = product.ratings.all()
        serializer = ProductRatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
