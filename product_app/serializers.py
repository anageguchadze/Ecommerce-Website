from rest_framework import serializers
from .models import Category, SubCategory, Product, Size, ImageSlider, ProductRating, ProductImage, Color
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

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    additional_images = ProductImageSerializer(many=True, read_only=True)
    color = ColorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class ImageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSlider
        fields = ['name', 'image']

    
class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Automatically set the user from the request

    class Meta:
        model = ProductRating
        fields = ['id', 'product', 'user', 'rating', 'created_at']