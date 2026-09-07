import random
import string
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MERCHANT = 'merchant', 'Merchant'
        CUSTOMER = 'customer', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_merchant(self):
        return self.role == self.Role.MERCHANT

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER


class EmailOTP(models.Model):
    class Purpose(models.TextChoices):
        SIGNUP = 'signup', 'Signup'
        PASSWORD_RESET = 'password_reset', 'Password Reset'

    email = models.EmailField()
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=Purpose.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} - {self.purpose}'

    @classmethod
    def generate_otp(cls):
        return ''.join(random.choices(string.digits, k=6))

    @classmethod
    def create_otp(cls, email, purpose, expiry_minutes=10):
        otp = cls.generate_otp()
        return cls.objects.create(
            email=email,
            otp=otp,
            purpose=purpose,
            expires_at=timezone.now() + timedelta(minutes=expiry_minutes),
        )

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
