from django.urls import path
from .views import RegisterView, LoginView, LogoutView, AddressView, PasswordChangeView, ProfileUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('address/', AddressView.as_view(), name='address_view'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
]
