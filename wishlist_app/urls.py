from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistItemViewSet

router = DefaultRouter()
router.register(r'items', WishlistItemViewSet, basename='wishlistitem')

urlpatterns = [
    path('', include(router.urls)),
    path('add_all_to_cart/', WishlistItemViewSet.as_view({'post': 'add_all_to_cart'}), name='add_all_to_cart'),
]
