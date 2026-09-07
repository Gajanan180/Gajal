from decimal import Decimal

from merchants.models import FoodItem


CART_SESSION_KEY = 'cart'


def get_cart(session):
    return session.setdefault(CART_SESSION_KEY, {})


def get_cart_items(session):
    cart = get_cart(session)
    items = []
    total = Decimal('0.00')
    store_id = None

    for food_id, qty in cart.items():
        try:
            food = FoodItem.objects.select_related('store').get(
                pk=int(food_id),
                is_available=True,
            )
        except (FoodItem.DoesNotExist, ValueError):
            continue
        subtotal = food.price * qty
        total += subtotal
        if store_id is None:
            store_id = food.store_id
        elif store_id != food.store_id:
            store_id = 'mixed'
        items.append({
            'food': food,
            'quantity': qty,
            'subtotal': subtotal,
        })

    return items, total, store_id


def add_to_cart(session, food_id, quantity=1):
    cart = get_cart(session)
    key = str(food_id)
    cart[key] = cart.get(key, 0) + quantity
    session.modified = True


def update_cart_item(session, food_id, quantity):
    cart = get_cart(session)
    key = str(food_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    session.modified = True


def clear_cart(session):
    session[CART_SESSION_KEY] = {}
    session.modified = True


def cart_count(session):
    cart = get_cart(session)
    return sum(cart.values())
