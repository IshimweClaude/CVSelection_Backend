from django import views
from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path('register', views.RegisterApiView.as_view(), name='register'),
    path('login', views.LoginApiView.as_view(), name='login'),
    path('user', views.AuthUserApiView.as_view(), name='user'),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.LogoutAPIView.as_view(), name='logout'),  
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name="request-reset-email"), 
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),   
    
]
