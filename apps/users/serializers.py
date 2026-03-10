from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from apps.users.models import User, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone', 'full_address']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 
                  'company_name', 'phone', 'contacts', 'is_email_verified']
        read_only_fields = ['id', 'is_email_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.is_email_verified = False
        
        # Генерируем токен подтверждения
        token = user.generate_verification_token()
        
        # Создаем ссылку для подтверждения
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}/"
        
        # Отправляем email с подтверждением
        send_mail(
            'Подтверждение email',
            f'Здравствуйте, {user.username}!\n\n'
            f'Для подтверждения email перейдите по ссылке:\n{verification_url}\n\n'
            f'Если вы не регистрировались, проигнорируйте это письмо.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return user

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)