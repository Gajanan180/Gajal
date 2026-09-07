from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import customer_required
from merchants.models import FoodItem, Store
from orders.cart import (
    add_to_cart,
    clear_cart,
    get_cart_items,
    update_cart_item,
)
from orders.forms import CheckoutForm
from orders.models import Order, OrderItem


@login_required
@customer_required
def add_to_cart_view(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id, is_available=True)
    _, _, store_id = get_cart_items(request.session)
    if store_id and store_id != 'mixed' and store_id != food.store_id:
        messages.warning(
            request,
            'Cart cleared — you can only order from one store at a time.',
        )
        clear_cart(request.session)
    add_to_cart(request.session, food_id)
    messages.success(request, f'{food.name} added to cart.')
    return redirect('merchants:store_detail', pk=food.store_id)


@login_required
@customer_required
def cart_view(request):
    items, total, store_id = get_cart_items(request.session)
    store = None
    if store_id and store_id != 'mixed':
        store = Store.objects.filter(pk=store_id).first()
    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total,
        'store': store,
        'mixed_stores': store_id == 'mixed',
    })


@login_required
@customer_required
def update_cart_view(request, food_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        update_cart_item(request.session, food_id, quantity)
        messages.success(request, 'Cart updated.')
    return redirect('orders:cart')


@login_required
@customer_required
def checkout_view(request):
    items, total, store_id = get_cart_items(request.session)
    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('home')
    if store_id == 'mixed':
        messages.error(request, 'Please order from one store at a time.')
        return redirect('orders:cart')

    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer=request.user,
                store=store,
                total_amount=total,
                delivery_address=form.cleaned_data['delivery_address'],
                notes=form.cleaned_data.get('notes', ''),
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    food_item=item['food'],
                    food_name=item['food'].name,
                    quantity=item['quantity'],
                    price=item['food'].price,
                )
            clear_cart(request.session)
            messages.success(request, 'Order placed! Proceed to payment.')
            return redirect('payments:pay', order_id=order.pk)
    else:
        form = CheckoutForm(initial={
            'delivery_address': getattr(request.user, 'store', None) and '' or '',
        })

    return render(request, 'orders/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'store': store,
    })


@login_required
def my_orders_view(request):
    if request.user.is_merchant:
        return redirect('merchants:orders')
    orders = request.user.orders.select_related('store').all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not (request.user == order.customer or request.user.is_superuser or
            (request.user.is_merchant and hasattr(request.user, 'store') and
             request.user.store == order.store)):
        messages.error(request, 'Access denied.')
        return redirect('home')
    return render(request, 'orders/order_detail.html', {'order': order})
