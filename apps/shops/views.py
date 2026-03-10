from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.shops.models import Shop, Category
from apps.shops.serializers import ShopSerializer, CategorySerializer

class IsSupplier(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_type == 'supplier'

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'toggle_status']:
            return [IsSupplier()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'supplier' and hasattr(user, 'shop'):
            return self.queryset.filter(id=user.shop.id)
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        # Проверяем, что пользователь - поставщик
        if request.user.user_type != 'supplier':
            return Response(
                {'error': 'Только поставщики могут создавать магазины'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем, что у пользователя еще нет магазина
        if hasattr(request.user, 'shop'):
            return Response(
                {'error': 'У вас уже есть магазин'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем магазин
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        shop = self.get_object()
        if shop.user != request.user:
            return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        shop.is_active = not shop.is_active
        shop.save()
        return Response({'is_active': shop.is_active})

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
