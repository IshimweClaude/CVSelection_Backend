
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=25, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=25, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'phone_number', 'user_role', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password from validated_data
        created_user = User.objects.create_user(**validated_data)

        if created_user.user_role == 'applicant':
            applicant = Applicant.objects.create(
                applicant=created_user)
        elif created_user.user_role == 'recruiter':
            recruiter = Recruiter.objects.create(recruiter=created_user)

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
