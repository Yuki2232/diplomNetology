from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.shops.views import ShopViewSet, CategoryViewSet

router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]