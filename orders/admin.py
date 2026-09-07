from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['food_name', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'store', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'store', 'created_at']
    search_fields = ['customer__username', 'store__name']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'food_name', 'quantity', 'price']
    search_fields = ['food_name', 'order__id']
