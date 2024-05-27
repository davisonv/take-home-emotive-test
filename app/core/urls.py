"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from two_factor_auth import views

router = DefaultRouter()

router.register('two-factor-auth', views.TwoFactorAuthenticationViewSet, basename='two_factor_auth')
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls))
]
