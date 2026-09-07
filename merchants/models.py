from django.conf import settings
from django.db import models


class Store(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='store',
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    cuisines = models.CharField(
        max_length=200,
        blank=True,
        default='indian biryani',
        help_text='Space-separated tags for filtering, e.g. indian biryani',
    )
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ['store', 'name']

    def __str__(self):
        return f'{self.name} ({self.store.name})'


class FoodItem(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='food_items',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='food_items',
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foods/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - ₹{self.price}'
