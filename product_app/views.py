from rest_framework import viewsets
from .models import Category, SubCategory, Product
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.utils import timezone
from datetime import timedelta


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


class NewArrivalsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Get the current date and time
        now = timezone.now()
        
        # Filter products created within the last 30 days
        thirty_days_ago = now - timedelta(days=30)
        return Product.objects.filter(created_at__gte=thirty_days_ago, is_active=True).order_by('-created_at')  # Order by latest first