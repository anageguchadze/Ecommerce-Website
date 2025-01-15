from rest_framework import serializers
from .models import Category, SubCategory, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer_product_app'

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested Category Serializer

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'description', 'image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        ref_name = 'ProductSerializer_product_app' 