from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('supplier', 'Поставщик'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='buyer')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.username}"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=20)
    structure = models.CharField(max_length=20, blank=True)
    building = models.CharField(max_length=20, blank=True)
    apartment = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    
    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}"
    
    @property
    def full_address(self):
        parts = [f"г. {self.city}", f"ул. {self.street}", f"д. {self.house}"]
        if self.structure:
            parts.append(f"корп. {self.structure}")
        if self.building:
            parts.append(f"стр. {self.building}")
        if self.apartment:
            parts.append(f"кв. {self.apartment}")
        return ", ".join(parts)
