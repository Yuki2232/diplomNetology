from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('shops/', include('apps.shops.urls')),
    path('products/', include('apps.products.urls')),
    path('orders/', include('apps.orders.urls')),
]