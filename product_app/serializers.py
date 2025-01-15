from rest_framework import serializers
from .models import Category, SubCategory, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested Category Serializer

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'description', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested Category Serializer
    subcategory = SubCategorySerializer()  # Nested SubCategory Serializer

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'subcategory', 'image', 'created_at', 'updated_at', 'is_active']
