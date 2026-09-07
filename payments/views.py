import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order
from payments.forms import PaymentForm
from payments.models import Payment


@login_required
def pay_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    if hasattr(order, 'payment') and order.payment.status == Payment.Status.SUCCESS:
        messages.info(request, 'This order is already paid.')
        return redirect('orders:order_detail', pk=order.pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment, _ = Payment.objects.get_or_create(
                order=order,
                defaults={'amount': order.total_amount},
            )
            payment.method = form.cleaned_data['method']
            payment.amount = order.total_amount
            payment.status = Payment.Status.SUCCESS
            payment.transaction_id = f'TXN-{uuid.uuid4().hex[:12].upper()}'
            if payment.method == Payment.Method.CARD:
                card_num = form.cleaned_data['card_number'].replace(' ', '')
                payment.card_last_four = card_num[-4:] if len(card_num) >= 4 else ''
            payment.save()
            order.status = Order.Status.CONFIRMED
            order.save()
            messages.success(request, 'Payment successful!')
            return redirect('payments:success', payment_id=payment.pk)
    else:
        form = PaymentForm()

    return render(request, 'payments/pay.html', {'form': form, 'order': order})


@login_required
def payment_success_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, order__customer=request.user)
    return render(request, 'payments/success.html', {'payment': payment})
