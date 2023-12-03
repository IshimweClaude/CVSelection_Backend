from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterApiView.as_view(), name='register'),
    path('login', views.LoginApiView.as_view(), name='login'),
    path('user', views.AuthUserApiView.as_view(), name='user'),

    path('countries', views.CountryApiView.as_view(), name='countries'),
    path('<int:id>', views.CountryDetailApiView.as_view(), name='country'),

    # path('token', jwt_views.TokenObtainPairView.as_view(), name='token'),
    # path('refresh', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
]
