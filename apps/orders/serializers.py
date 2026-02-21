from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.users.serializers import ContactSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'product_name', 'quantity', 'price', 'total_sum']
        read_only_fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    contact_details = ContactSerializer(source='contact', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'contact', 'contact_details', 'status', 'items', 'total_sum', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class OrderListSerializer(serializers.ModelSerializer):
    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_sum', 'created_at']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден")
        
        if product.quantity < self.initial_data.get('quantity', 1):
            raise serializers.ValidationError(f"Доступно только {product.quantity} шт.")
        
        return value

class OrderConfirmSerializer(serializers.Serializer):
    contact_id = serializers.IntegerField()
    
    def validate_contact_id(self, value):
        user = self.context['request'].user
        if not user.contacts.filter(id=value).exists():
            raise serializers.ValidationError("Контакт не найден")
        return value

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']