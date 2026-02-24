from django.contrib import admin
from apps.users.models import User, Contact

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'user_type', 'phone']
    list_filter = ['user_type']
    search_fields = ['username', 'email']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'street', 'house', 'phone']
    list_filter = ['city']
    search_fields = ['user__username', 'city']
