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
        
        # Проверка наличия товара (без списания)
        if product.quantity < quantity:
            return Response(
                {'error': f'Недостаточно товара. Доступно: {product.quantity}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
        
        # НЕ УМЕНЬШАЕМ КОЛИЧЕСТВО ТОВАРА НА СКЛАДЕ
        # Товар резервируется только при подтверждении заказа
        
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
        
        # НЕ ВОЗВРАЩАЕМ ТОВАР НА СКЛАД, ТАК КАК ОН НЕ БЫЛ СПИСАН
        item.delete()
        
        return Response(OrderSerializer(cart).data)
    
    @action(detail=False, methods=['post'])
    def confirm(self, request):
        cart = Order.objects.filter(user=request.user, status='basket').first()
        
        if not cart or not cart.items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderConfirmSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Проверка наличия всех товаров перед списанием
        for item in cart.items.all():
            product = item.product
            if product.quantity < item.quantity:
                return Response({
                    'error': f'Товара "{product.name}" недостаточно на складе. Доступно: {product.quantity}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # СПИСЫВАЕМ ТОВАРЫ СО СКЛАДА
        for item in cart.items.all():
            product = item.product
            product.quantity -= item.quantity
            product.save()
        
        cart.contact_id = serializer.validated_data['contact_id']
        cart.status = 'new'
        cart.save()
        
        # Отправка email клиенту
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
        
        # Отправка email администратору
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
        
        old_status = order.status
        new_status = serializer.validated_data['status']
        order.status = new_status
        order.save()
        
        # Если заказ отменяется - возвращаем товары на склад
        if new_status == 'canceled' and old_status != 'canceled':
            for item in order.items.all():
                product = item.product
                product.quantity += item.quantity
                product.save()
        
        # Отправка уведомления клиенту
        send_mail(
            f'Статус заказа №{order.id} изменен',
            f'Здравствуйте, {order.user.username}!\n\n'
            f'Статус вашего заказа №{order.id} изменен на: {order.get_status_display()}',
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False,
        )
        
        return Response({
            'status': order.status,
            'message': 'Статус заказа успешно обновлен'
        })
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
