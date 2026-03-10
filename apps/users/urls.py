from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet, RegisterView, ContactViewSet, CustomAuthToken
from apps.users.verification import verify_email

router = DefaultRouter()
router.register('profile', UserViewSet)
router.register('contacts', ContactViewSet, basename='contacts')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('verify-email/<str:token>/', verify_email, name='verify-email'),
]