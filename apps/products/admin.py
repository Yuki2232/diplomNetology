from django.contrib import admin
from apps.products.models import Product, ProductParameter

class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'shop', 'category', 'price', 'quantity', 'gender', 'is_active']
    list_filter = ['shop', 'category', 'gender', 'is_active']
    search_fields = ['name', 'description']
    inlines = [ProductParameterInline]

@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'value']
    list_filter = ['name']
    search_fields = ['product__name', 'value']
