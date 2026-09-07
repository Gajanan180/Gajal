from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import merchant_required
from merchants.forms import CategoryForm, FoodItemForm, StoreForm
from merchants.models import Category, FoodItem, Store
from orders.models import Order


def home_view(request):
    stores = Store.objects.filter(is_active=True).select_related('owner')
    user_store = None
    if request.user.is_authenticated and request.user.is_merchant:
        user_store = Store.objects.filter(owner=request.user).first()
    return render(request, 'home.html', {
        'stores': stores,
        'user_store': user_store,
    })


@merchant_required
def dashboard_view(request):
    store = Store.objects.filter(owner=request.user).first()
    orders = Order.objects.none()
    food_count = 0
    if store:
        orders = store.orders.all()[:10]
        food_count = store.food_items.count()
    return render(request, 'merchants/dashboard.html', {
        'store': store,
        'orders': orders,
        'food_count': food_count,
    })


@merchant_required
def store_setup_view(request):
    store = Store.objects.filter(owner=request.user).first()
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store_obj = form.save(commit=False)
            store_obj.owner = request.user
            store_obj.save()
            messages.success(request, 'Store saved successfully!')
            return redirect('merchants:dashboard')
    else:
        form = StoreForm(instance=store)

    return render(request, 'merchants/store_form.html', {'form': form, 'store': store})


@merchant_required
def food_list_view(request):
    store = get_object_or_404(Store, owner=request.user)
    foods = store.food_items.select_related('category').all()
    return render(request, 'merchants/food_list.html', {'store': store, 'foods': foods})


@merchant_required
def food_create_view(request):
    store = get_object_or_404(Store, owner=request.user)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, store=store)
        if form.is_valid():
            food = form.save(commit=False)
            food.store = store
            food.save()
            messages.success(request, 'Food item added!')
            return redirect('merchants:food_list')
    else:
        form = FoodItemForm(store=store)

    return render(request, 'merchants/food_form.html', {'form': form, 'title': 'Add Food Item'})


@merchant_required
def food_edit_view(request, pk):
    store = get_object_or_404(Store, owner=request.user)
    food = get_object_or_404(FoodItem, pk=pk, store=store)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food, store=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item updated!')
            return redirect('merchants:food_list')
    else:
        form = FoodItemForm(instance=food, store=store)

    return render(request, 'merchants/food_form.html', {'form': form, 'title': 'Edit Food Item'})


@merchant_required
def food_delete_view(request, pk):
    store = get_object_or_404(Store, owner=request.user)
    food = get_object_or_404(FoodItem, pk=pk, store=store)
    if request.method == 'POST':
        food.delete()
        messages.success(request, 'Food item deleted.')
        return redirect('merchants:food_list')
    return render(request, 'merchants/food_confirm_delete.html', {'food': food})


@merchant_required
def category_manage_view(request):
    store = get_object_or_404(Store, owner=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.store = store
            category.save()
            messages.success(request, 'Category added!')
            return redirect('merchants:categories')
    else:
        form = CategoryForm()

    categories = store.categories.all()
    return render(request, 'merchants/category_list.html', {
        'store': store,
        'categories': categories,
        'form': form,
    })


@merchant_required
def order_manage_view(request):
    store = get_object_or_404(Store, owner=request.user)
    orders = store.orders.select_related('customer').all()
    return render(request, 'merchants/order_list.html', {'store': store, 'orders': orders})


@merchant_required
def order_update_status_view(request, pk):
    store = get_object_or_404(Store, owner=request.user)
    order = get_object_or_404(Order, pk=pk, store=store)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.pk} updated to {order.get_status_display()}.')
        return redirect('merchants:orders')
    return render(request, 'merchants/order_detail.html', {'order': order})


from orders.cart import get_cart_items


def store_detail_view(request, pk):
    store = get_object_or_404(Store, pk=pk, is_active=True)
    foods = store.food_items.filter(is_available=True).select_related('category')
    categories = store.categories.all()
    cart_items, cart_total, cart_store_id = get_cart_items(request.session)
    store_cart_items = [i for i in cart_items if i['food'].store_id == store.pk]
    return render(request, 'merchants/store_detail.html', {
        'store': store,
        'foods': foods,
        'categories': categories,
        'cart_items': store_cart_items,
        'cart_total': sum(i['subtotal'] for i in store_cart_items),
    })
