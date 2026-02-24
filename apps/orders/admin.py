from django.contrib import admin
from apps.orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'shop', 'quantity', 'price', 'total_sum']
    
    def total_sum(self, obj):
        return obj.total_sum
    total_sum.short_description = 'Сумма'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contact', 'status', 'total_sum', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_sum']
    inlines = [OrderItemInline]
    
    def total_sum(self, obj):
        return obj.total_sum
    total_sum.short_description = 'Общая сумма'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'shop', 'quantity', 'price', 'total_sum']
    list_filter = ['shop']
    search_fields = ['product__name', 'order__id']
    
    def total_sum(self, obj):
        return obj.total_sum
    total_sum.short_description = 'Сумма'
