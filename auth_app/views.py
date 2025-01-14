from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout

# Register View (no changes here)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # User is validated, now we can generate a token
            user = serializer.validated_data  # Returns the user from the serializer

            try:
                # Generate JWT token
                refresh = RefreshToken.for_user(user)  # This creates a refresh token
                access_token = refresh.access_token  # This creates an access token from the refresh token

                # Return both access and refresh tokens
                return Response({
                    "access": str(access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Token generation failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Logout View (Invalidate refresh token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication to log out

    def post(self, request):
        # Logout the user and blacklist the refresh token
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist refresh token for security

            # Log out the user from the session
            logout(request)

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
