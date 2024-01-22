from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from requests import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import User, Country
from .serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LogoutSerializer
    
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.permissions import AllowAny, IsAuthenticated
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import views
from rest_framework import generics, status
from django.http import Http404
from authentication.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

from rest_framework.authentication import TokenAuthentication

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
        if user is None:
            return response.Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.email_verified:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response({'error': 'Email is not verified'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # simply delete the token to force a login
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    
    def post(self, request):
        # data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                'password-reset-confirm',kwargs={'uidb64':uidb64, 'token':token})
            absurl = 'http://'+current_site+relative_link
            email_body = 'Hello, \n Use link below to reset your password \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Reset your password'}
            Util.send_email(data)
        return response.Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(GenericAPIView):
    def get(self, request, uid64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response ({'success':True, 'message':'Credentials Valid', 'uidb64':uid64, 'token':token}, status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return response.Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)    
        
        
class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return response.Response({'success':True, 'message':'Password reset success'}, status=status.HTTP_200_OK)