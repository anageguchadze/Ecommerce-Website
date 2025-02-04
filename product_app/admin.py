from django.contrib import admin
from .models import Category, SubCategory, Product, Size, ImageSlider, ProductRating, ProductImage, Color

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(ImageSlider)
admin.site.register(ProductRating)
admin.site.register(ProductImage)
admin.site.register(Color)