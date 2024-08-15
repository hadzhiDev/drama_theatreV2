from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

from .views import GoogleAuthAPIView, get_google_code

router = DefaultRouter()
router.register('profile', views.ProfileViewSet)


urlpatterns = [
    path('login/', views.LoginGenericAPIView.as_view()),
    path('register/', views.RegisterGenericApiView.as_view()),
    path('change-password/', views.ChangePasswordApiView.as_view()),
    path('send-reset-password-key/', views.SendResetPasswordKeyApiView.as_view()),
    path('reset-password/', views.ResetPasswordApiView.as_view()),
    path('', include(router.urls)),
    path('google-auth/', GoogleAuthAPIView.as_view()),
    path('getcode-goole/', get_google_code, name='get-code'),
]