
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, Token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=25, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=25, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'user_role', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        data['user_role'] = data.get('user_role', 'applicant') # Set default user_role to applicant

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password from validated_data
        created_user = User.objects.create_user(**validated_data)

        # Try to create an associated Applicant or Recruiter
        try:
            if created_user.user_role == 'applicant':
                applicant = Applicant.objects.create(applicant=created_user)
            elif created_user.user_role == 'recruiter':
                recruiter = Recruiter.objects.create(recruiter=created_user)
        except Exception as e:
            # Handle the exception (e.g., log the error)
            # You might want to delete the user or take appropriate action
            print(str(e))
            created_user.delete()
            raise serializers.ValidationError("Failed to create associated profile.")

        return created_user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=25, min_length=6, write_only=True)

    class Meta:
        model = User

        fields = ['email', 'password', 'token',
                  'user_role', 'first_name', 'last_name']
        read_only_fields = ['token', 'user_role', 'first_name', 'last_name']

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=25, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)
            
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')