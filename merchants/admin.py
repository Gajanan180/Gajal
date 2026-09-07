from django.contrib import admin

from .models import Category, FoodItem, Store


class FoodItemInline(admin.TabularInline):
    model = FoodItem
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'owner__username', 'address']
    inlines = [CategoryInline, FoodItemInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'store']
    list_filter = ['store']
    search_fields = ['name', 'store__name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'category', 'price', 'is_available']
    list_filter = ['store', 'is_available', 'category']
    search_fields = ['name', 'store__name']
