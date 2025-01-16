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
    average_rating = serializers.IntegerField(source='review')  # Directly show the review value
    votes = serializers.SerializerMethodField()  # We will count votes based on reviews.

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'final_price', 'stock', 'category', 'subcategory', 'image', 'average_rating', 'votes', 'size']

    def get_votes(self, obj):
        # Since we're not using a list, we just return 1 if there's a review
        return 1 if obj.review > 0 else 0

