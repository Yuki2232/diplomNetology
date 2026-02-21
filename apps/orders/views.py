from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.orders.serializers import (
    OrderSerializer, OrderListSerializer, AddToCartSerializer,
    OrderConfirmSerializer, OrderStatusSerializer
)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'supplier' and hasattr(user, 'shop'):
            return Order.objects.filter(items__shop=user.shop).distinct()
        return Order.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['get'])
    def cart(self, request):
        cart, created = Order.objects.get_or_create(
            user=request.user,
            status='basket'
        )
        serializer = OrderSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        
        cart, _ = Order.objects.get_or_create(
            user=request.user,
            status='basket'
        )
        
        order_item, created = OrderItem.objects.get_or_create(
            order=cart,
            product=product,
            shop=product.shop,
            defaults={'quantity': quantity, 'price': product.price}
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        product.quantity -= quantity
        product.save()
        
        return Response(OrderSerializer(cart).data)
    
    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({'error': 'Не указан product_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = Order.objects.filter(user=request.user, status='basket').first()
        
        if not cart:
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_404_NOT_FOUND)
        
        item = get_object_or_404(OrderItem, order=cart, product_id=product_id)
        
        product = item.product
        product.quantity += item.quantity
        product.save()
        
        item.delete()
        
        return Response(OrderSerializer(cart).data)
    
    @action(detail=False, methods=['post'])
    def confirm(self, request):
        cart = Order.objects.filter(user=request.user, status='basket').first()
        
        if not cart or not cart.items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderConfirmSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        cart.contact_id = serializer.validated_data['contact_id']
        cart.status = 'new'
        cart.save()
        
        send_mail(
            'Подтверждение заказа',
            f'Здравствуйте, {request.user.username}!\n\n'
            f'Ваш заказ №{cart.id} оформлен.\n'
            f'Сумма заказа: {cart.total_sum} руб.\n'
            f'Статус заказа: Новый\n\n'
            f'Мы свяжемся с вами для подтверждения.',
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
        
        send_mail(
            f'Новый заказ №{cart.id}',
            f'Новый заказ от пользователя {request.user.username}\n'
            f'Сумма: {cart.total_sum} руб.\n'
            f'Адрес доставки: {cart.contact.full_address}\n'
            f'Телефон: {cart.contact.phone}',
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        return Response(OrderSerializer(cart).data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        
        if request.user.user_type != 'supplier' and not request.user.is_staff:
            return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order.status = serializer.validated_data['status']
        order.save()
        
        send_mail
