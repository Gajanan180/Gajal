from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EmailOTP, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Gajal Profile', {'fields': ('role', 'phone', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Gajal Profile', {'fields': ('role', 'phone', 'email')}),
    )


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp', 'purpose', 'is_used', 'created_at', 'expires_at']
    list_filter = ['purpose', 'is_used']
    search_fields = ['email', 'otp']
    readonly_fields = ['created_at']
