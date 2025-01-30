from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, LoginSerializer, PasswordChangeSerializer, AddressSerializer, ProfileUpdateSerializer, GoogleAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework.generics import GenericAPIView
from django.contrib.auth import update_session_auth_hash
from .models import Address, CustomUser
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can change their password

    def post(self, request):
        user = request.user  # The currently authenticated user
        serializer = PasswordChangeSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            # Set the new password and save the user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            # Update session authentication hash to keep the user logged in after changing the password
            update_session_auth_hash(request, user)

            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddressView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can interact with addresses

    def get(self, request):
        # Fetch the user's address (assuming one address per user)
        address = Address.objects.filter(user=request.user).first()
        
        if address:
            serializer = AddressSerializer(address)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No address found for this user."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Create or update the address (if it exists, update it)
        address, created = Address.objects.get_or_create(user=request.user)
        
        # Now, handle the POST request to create or update the address
        serializer = AddressSerializer(address, data=request.data, partial=True)  # `partial=True` allows updating fields
        if serializer.is_valid():
            serializer.save()  # Save the new or updated address
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the current user's profile
        user = request.user
        serializer = ProfileUpdateSerializer(user)
        return Response(serializer.data, status=200)

    def put(self, request):
        # Update the user's profile
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=200)
        return Response(serializer.errors, status=400)
    


class GoogleAuthView(GenericAPIView):
    """
    POST endpoint to exchange a Google ID token for our own JWT tokens.
    """
    serializer_class = GoogleAuthSerializer

    def post(self, request, *args, **kwargs):
        # 1. Validate incoming data (which should contain the 'id_token')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_token_value = serializer.validated_data.get('id_token')
        
        try: 
            # 2. Verify the token using Google's library
            #    You must pass the same 'audience' as your front-end's OAuth 2.0 client ID
            google_info = id_token.verify_oauth2_token(
                id_token_value,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=200 
            )
        except ValueError as e:
            # Token is invalid
            return Response({"detail": "Invalid Google token."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. google_info will contain user details from Google if token is valid
        #    typical fields: 'email', 'email_verified', 'sub' (unique user id from Google), 'name', 'picture', etc.

        google_email = google_info.get('email')

        # You could also check google_info.get('email_verified') if needed.
        
        if not google_email:
            return Response({"detail": "No email found in Google token."}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Create or retrieve the user from the DB
        user, created = CustomUser.objects.get_or_create(email=google_email)
        
        # If user was newly created, optionally create the verification code entry
        if created:
            user.set_password('admin123@@')  # Set a random password
            user.save()
        
        # 5. Generate JWT tokens via SimpleJWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 6. Return tokens
        return Response({
            "refresh": str(refresh),
            "access": access_token,
            "email": user.email,
        }, status=status.HTTP_200_OK)
