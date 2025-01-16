from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet, CouponViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'coupons', CouponViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
