from decimal import Decimal
from pathlib import Path

from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import User
from merchants.models import Category, FoodItem, Store

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
STATIC_IMG = BASE_DIR / 'static' / 'img'

FOOD_MENU = [
    ('Biryani', [
        ('Hyderabadi Chicken Biryani', 'Aromatic basmati rice with tender chicken and saffron', Decimal('299'), 'biryani-chicken.jpg'),
        ('Mutton Dum Biryani', 'Slow-cooked mutton biryani with rich spices', Decimal('349'), 'biryani-mutton.jpg'),
        ('Paneer Biryani', 'Fragrant veg biryani with cottage cheese cubes', Decimal('249'), 'biryani-veg.jpg'),
        ('Egg Biryani', 'Spiced rice layered with boiled eggs', Decimal('199'), 'biryani-egg.jpg'),
        ('Veg Dum Biryani', 'Mixed vegetables with long-grain basmati rice', Decimal('219'), 'biryani-veg.jpg'),
    ]),
    ('Main Course', [
        ('Butter Chicken', 'Creamy tomato gravy with tandoori chicken', Decimal('279'), 'butter-chicken.jpg'),
        ('Paneer Butter Masala', 'Rich creamy paneer curry', Decimal('249'), 'paneer.jpg'),
        ('Dal Makhani', 'Slow-cooked black lentils in butter and cream', Decimal('189'), 'dal.jpg'),
        ('Chicken Tikka Masala', 'Grilled chicken in spiced tomato gravy', Decimal('289'), 'tikka.jpg'),
        ('Palak Paneer', 'Fresh spinach with soft paneer cubes', Decimal('229'), 'paneer.jpg'),
    ]),
    ('Breads & Rice', [
        ('Garlic Naan', 'Soft tandoori naan with garlic butter', Decimal('49'), 'naan.jpg'),
        ('Butter Naan', 'Classic tandoori butter naan', Decimal('45'), 'naan.jpg'),
        ('Jeera Rice', 'Basmati rice tempered with cumin', Decimal('99'), 'rice.jpg'),
    ]),
    ('Desserts', [
        ('Gulab Jamun', 'Soft milk dumplings in sugar syrup (2 pcs)', Decimal('79'), 'gulab.jpg'),
        ('Rasmalai', 'Soft cottage cheese discs in sweet milk (2 pcs)', Decimal('99'), 'rasmalai.jpg'),
        ('Kheer', 'Traditional rice pudding with nuts', Decimal('89'), 'kheer.jpg'),
    ]),
]


class Command(BaseCommand):
    help = 'Seed Kajal merchant using local images from static/img (no internet needed)'

    def handle(self, *args, **options):
        self.stdout.write('Generating local images (offline, no download)...')
        call_command('generate_images')

        email = 'gajananpathak09@gmail.com'
        username = 'kajal'

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'role': User.Role.MERCHANT,
                'is_verified': True,
                'phone': '9876543210',
            },
        )
        if created:
            user.set_password('Kajal@123')
        user.role = User.Role.MERCHANT
        user.is_verified = True
        user.save()

        store, _ = Store.objects.get_or_create(
            owner=user,
            defaults={
                'name': 'Kajal',
                'description': 'Authentic Indian cuisine & legendary biryanis. Home-style recipes, premium ingredients.',
                'address': 'Shop 12, FC Road, Pune, Maharashtra 411005',
                'phone': '9876543210',
                'cuisines': 'indian biryani north indian',
                'is_active': True,
            },
        )
        store.name = 'Kajal'
        store.cuisines = 'indian biryani north indian'
        store.is_active = True
        store.save()

        attached = 0
        store_img = STATIC_IMG / 'stores' / 'kajal.jpg'
        if store_img.exists():
            with open(store_img, 'rb') as f:
                store.image.save('kajal.jpg', File(f), save=True)
            attached += 1
            self.stdout.write(f'  Store image: {store_img.name}')

        FoodItem.objects.filter(store=store).delete()
        Category.objects.filter(store=store).delete()

        total = 0
        for cat_name, items in FOOD_MENU:
            category = Category.objects.create(store=store, name=cat_name)
            for name, desc, price, img_file in items:
                food = FoodItem.objects.create(
                    store=store,
                    category=category,
                    name=name,
                    description=desc,
                    price=price,
                    is_available=True,
                )
                img_path = STATIC_IMG / 'foods' / img_file
                if img_path.exists():
                    with open(img_path, 'rb') as f:
                        food.image.save(img_file, File(f), save=False)
                        food.save()
                    attached += 1
                total += 1

        self.stdout.write(self.style.SUCCESS(
            f'Kajal ready: {total} menu items, {attached} images attached from static/img/'
        ))
        self.stdout.write(f'Login: {username} / Kajal@123')
        self.stdout.write('Tip: Upload real photos via Merchant Dashboard -> My Menu -> Edit')
