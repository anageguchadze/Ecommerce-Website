from rest_framework import serializers
from .models import Category, SubCategory, Product, Size

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer_product_app'

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested Category Serializer

    class Meta:
        model = SubCategory
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'