from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, NewArrivalsView, BestSellersView, ImageSliderListView, ProductRatingView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)), 
    path('new-arrivals/', NewArrivalsView.as_view(), name='new_arrivals'), 
    path('best-sellers/', BestSellersView.as_view(), name='best_sellers'),
    path('image-sliders/', ImageSliderListView.as_view(), name='image_slider_list'),
    path('products/<int:product_id>/rate/', ProductRatingView.as_view(), name='product_rating'),
]
