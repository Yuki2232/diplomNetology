from rest_framework import serializers
from apps.shops.models import Shop, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class ShopSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'user', 'is_active', 'categories', 'created_at']
        read_only_fields = ['id', 'created_at']