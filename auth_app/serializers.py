from rest_framework import serializers
from .models import CustomUser, Address
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()  # Accepts either email or phone number
    password = serializers.CharField()

    def validate(self, data):
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')

        # Check if it's an email or phone number
        if '@' in email_or_phone:
            user = CustomUser.objects.filter(email=email_or_phone).first()  # Find by email
        else:
            user = CustomUser.objects.filter(phone_number=email_or_phone).first()  # Find by phone number

        if user is None:
            raise serializers.ValidationError("User not found")
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        # Return the user instance for token generation in view
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Validate current password
        user = self.context.get('user')  # Access the authenticated user
        if not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect.")

        # Validate new password matches the confirm password
        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match.")

        # Validate new password strength
        try:
            password_validation.validate_password(new_password, user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return attrs
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'country', 'zip_code', 'is_primary']

    def create(self, validated_data):
        # Create a new address for the user
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user
        return super().create(validated_data)


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    # Include the address serializer to show the user's addresses as well
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'addresses']
        

class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()  # Email is read-only
    phone_number = serializers.ReadOnlyField()  # Phone number is read-only

    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'email', 'phone_number']

    def update(self, instance, validated_data):
        # Update user details
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
    

class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)

    def validate(self, attrs):
        id_token = attrs.get('id_token')
        if not id_token:
            raise serializers.ValidationError({"id_token": "Missing Google ID token."})
        return attrs