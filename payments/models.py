from django.db import models

from orders.models import Order


class Payment(models.Model):
    class Method(models.TextChoices):
        GPAY = 'gpay', 'Google Pay'
        PHONEPE = 'phonepe', 'PhonePe'
        CARD = 'card', 'Credit/Debit Card'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
    )
    method = models.CharField(max_length=20, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    transaction_id = models.CharField(max_length=100, blank=True)
    card_last_four = models.CharField(max_length=4, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment #{self.pk} - {self.get_method_display()} ({self.status})'
