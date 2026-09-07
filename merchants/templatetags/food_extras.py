from django import template
from django.templatetags.static import static

register = template.Library()

STORE_DEFAULT = 'img/stores/kajal.jpg'

FOOD_IMAGE_MAP = {
    'hyderabadi chicken biryani': 'img/foods/biryani-chicken.jpg',
    'mutton dum biryani': 'img/foods/biryani-mutton.jpg',
    'paneer biryani': 'img/foods/biryani-veg.jpg',
    'egg biryani': 'img/foods/biryani-egg.jpg',
    'veg dum biryani': 'img/foods/biryani-veg.jpg',
    'butter chicken': 'img/foods/butter-chicken.jpg',
    'paneer butter masala': 'img/foods/paneer.jpg',
    'dal makhani': 'img/foods/dal.jpg',
    'chicken tikka masala': 'img/foods/tikka.jpg',
    'palak paneer': 'img/foods/paneer.jpg',
    'garlic naan': 'img/foods/naan.jpg',
    'butter naan': 'img/foods/naan.jpg',
    'jeera rice': 'img/foods/rice.jpg',
    'gulab jamun': 'img/foods/gulab.jpg',
    'rasmalai': 'img/foods/rasmalai.jpg',
    'kheer': 'img/foods/kheer.jpg',
}


@register.filter
def store_image(store):
    if store.image:
        return store.image.url
    name = store.name.lower()
    if 'kajal' in name:
        return static('img/stores/kajal.jpg')
    return static(STORE_DEFAULT)


@register.filter
def food_image(food):
    if food.image:
        return food.image.url
    key = food.name.lower()
    for pattern, path in FOOD_IMAGE_MAP.items():
        if pattern in key or key in pattern:
            return static(path)
    if 'biryani' in key:
        return static('img/foods/biryani-chicken.jpg')
    if any(k in key for k in ('naan', 'roti', 'rice')):
        return static('img/foods/rice.jpg')
    if any(k in key for k in ('chicken', 'tikka', 'curry')):
        return static('img/foods/butter-chicken.jpg')
    if 'paneer' in key:
        return static('img/foods/paneer.jpg')
    if any(k in key for k in ('dal', 'makhani')):
        return static('img/foods/dal.jpg')
    if any(k in key for k in ('gulab', 'jamun', 'rasmalai', 'kheer')):
        return static('img/foods/gulab.jpg')
    return static('img/foods/butter-chicken.jpg')


@register.filter
def rating_display(pk):
    return f'4.{(pk % 5) + 4}'


@register.filter
def offer_text(pk):
    offers = ['50% OFF up to ₹100', 'Flat ₹75 OFF', 'Free Delivery', '30% OFF', 'Buy 1 Get 1']
    return offers[pk % len(offers)]


@register.filter
def cost_for_two(pk):
    base = 200 + (pk * 47) % 300
    return f'₹{base} for two'


@register.filter
def delivery_time(pk):
    times = ['25–30 mins', '30–35 mins', '20–25 mins', '35–40 mins']
    return times[pk % len(times)]


@register.filter
def cuisine_display(cuisines):
    if not cuisines:
        return 'North Indian, Biryani'
    return ', '.join(c.title() for c in cuisines.split())
