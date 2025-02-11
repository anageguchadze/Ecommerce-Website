from rest_framework import serializers
from .models import Category, SubCategory, Product, Size, ImageSlider, ProductRating, ProductImage, Color
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer_product_app'

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer() 

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

class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = ProductRating
        fields = ['id', 'product', 'user', 'rating']
    


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    additional_images = ProductImageSerializer(many=True, read_only=True)
    color = ColorSerializer(many=True, read_only=True)
    ratings = ProductRatingSerializer(many=True, read_only=True)
    vote_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ratings'] = ProductRating.objects.filter(product=instance).aggregate(Avg('rating'))['rating__avg']
        representation['vote_count'] = ProductRating.objects.filter(product=instance).count()
        return representation


class ImageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSlider
        fields = ['name', 'image']

    
