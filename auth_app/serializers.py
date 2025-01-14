from rest_framework import serializers
from .models import CustomUser

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

