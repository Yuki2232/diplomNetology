from rest_framework import serializers
from apps.products.models import Product, ProductParameter

class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    parameters = ProductParameterSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'shop', 'shop_name', 
                 'description', 'price', 'quantity', 'gender', 'parameters']
        read_only_fields = ['id']