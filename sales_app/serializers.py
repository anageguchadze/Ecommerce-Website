from rest_framework import serializers
from .models import Sale, Discount
from product_app.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        ref_name = 'ProductSerializer_sales_app'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer_sales_app'

class SaleSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'name', 'description', 'discount_percentage', 'discount_amount', 
                  'start_date', 'end_date', 'is_active', 'products']

class DiscountSerializer(serializers.ModelSerializer):
    applicable_categories = CategorySerializer(many=True, read_only=True)
    applicable_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Discount
        fields = ['id', 'discount_type', 'discount_value', 'start_date', 'end_date', 
                  'applicable_categories', 'applicable_products']
