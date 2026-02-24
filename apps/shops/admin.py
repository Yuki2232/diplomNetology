from django.contrib import admin
from apps.shops.models import Shop, Category

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'user__username']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    filter_horizontal = ['shops']