from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/google/', GoogleLoginAPIView.as_view(), name='google-login'),
]

