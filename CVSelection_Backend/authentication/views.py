from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from requests import Response
from rest_framework.generics import GenericAPIView

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import views
# Create your views here.


class AuthUserApiView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({"user": serializer.data})


class RegisterApiView(GenericAPIView):
    authentication_classes = []

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            user_data = authenticate(
                email=user['email'], password=user['password'])
            token = user_data.token
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            absurl = 'http://'+current_site+relative_link+"?token="+str(token)
            email_body = 'Hi ' + user['username'] + \
                ' use link below to verify your email \n' + absurl
            data = {'email_body': email_body,
                    'email_subject': 'Verify your email', 'to_email': user['email']}
            Util.send_email(data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer
    authentication_classes = []

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(email=payload['email'])
            if not user.email_verified:
                user.email_verified = True
                user.save()

            return response.Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return response.Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user.email_verified:
            if user:
                serializer = self.serializer_class(user)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            return response.Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return response.Response({'error': 'Email is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
