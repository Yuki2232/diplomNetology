from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from apps.users.models import Contact
from apps.users.serializers import UserSerializer, RegisterSerializer, ContactSerializer, ContactCreateSerializer
from apps.shops.models import Shop
from apps.shops.serializers import ShopSerializer

User = get_user_model()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'user_type': user.user_type,
            'is_email_verified': user.is_email_verified
        })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def become_supplier(self, request):
        user = request.user
        
        if user.user_type == 'supplier':
            return Response({'error': 'Вы уже являетесь поставщиком'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_email_verified:
            return Response({'error': 'Необходимо подтвердить email'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.user_type = 'supplier'
        user.save()
        
        # Создаем магазин автоматически или возвращаем успех
        if not hasattr(user, 'shop'):
            shop = Shop.objects.create(
                name=f"Магазин {user.username}",
                user=user,
                is_active=True
            )
            serializer = ShopSerializer(shop)
            return Response({
                'message': 'Вы стали поставщиком',
                'shop': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({'message': 'Вы стали поставщиком'}, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.contacts.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactCreateSerializer
        return ContactSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)