from django.db import models
from apps.users.models import User

class Shop(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    shops = models.ManyToManyField(Shop, related_name='categories')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
