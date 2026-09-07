from pathlib import Path

from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

FOOD_COLORS = {
    'biryani-chicken': (139, 58, 18),
    'biryani-mutton': (110, 45, 15),
    'biryani-veg': (22, 101, 52),
    'biryani-egg': (180, 83, 9),
    'butter-chicken': (194, 65, 12),
    'paneer': (234, 88, 12),
    'dal': (120, 72, 8),
    'tikka': (185, 55, 20),
    'naan': (210, 105, 20),
    'rice': (160, 82, 22),
    'gulab': (168, 28, 88),
    'rasmalai': (218, 165, 32),
    'kheer': (180, 120, 40),
}

CUISINE_COLORS = {
    'all': (252, 128, 25),
    'indian': (194, 65, 12),
    'biryani': (139, 58, 18),
    'pizza': (220, 60, 20),
    'burger': (180, 90, 25),
    'chinese': (200, 45, 45),
    'dessert': (190, 50, 100),
}

FOOD_EMOJI = {
    'biryani-chicken': '🍗', 'biryani-mutton': '🥘', 'biryani-veg': '🥗', 'biryani-egg': '🥚',
    'butter-chicken': '🍛', 'paneer': '🧀', 'dal': '🫘', 'tikka': '🍢',
    'naan': '🫓', 'rice': '🍚', 'gulab': '🍡', 'rasmalai': '🍮', 'kheer': '🥣',
}

CUISINE_EMOJI = {
    'all': '🍽', 'indian': '🍛', 'biryani': '🍚', 'pizza': '🍕',
    'burger': '🍔', 'chinese': '🥡', 'dessert': '🍰',
}


def _fonts(large_size, small_size, emoji_size):
    try:
        return (
            ImageFont.truetype('arial.ttf', large_size),
            ImageFont.truetype('arial.ttf', small_size),
            ImageFont.truetype('seguiemj.ttf', emoji_size),
        )
    except OSError:
        default = ImageFont.load_default()
        return default, default, default


def draw_food_card(path, title, subtitle, color, emoji, size):
    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = size
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)

    for i in range(h):
        t = i / h
        r = int(color[0] * (1 - t * 0.3) + 20 * t)
        g = int(color[1] * (1 - t * 0.3) + 15 * t)
        b = int(color[2] * (1 - t * 0.3) + 10 * t)
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    draw.ellipse([(w * 0.15, h * 0.08), (w * 0.85, h * 0.72)], fill=(255, 255, 255, 30), outline=(255, 255, 255, 80))

    font_l, font_s, font_e = _fonts(26 if w > 250 else 16, 13 if w > 250 else 9, 48 if w > 250 else 32)
    draw.text((w // 2, h * 0.32), emoji, fill='white', anchor='mm', font=font_e)
    draw.text((w // 2, h * 0.58), title, fill='white', anchor='mm', font=font_l)
    draw.text((w // 2, h * 0.72), subtitle, fill=(255, 235, 210), anchor='mm', font=font_s)

    badge = 'Gajal Food'
    draw.rounded_rectangle([(w * 0.05, h * 0.04), (w * 0.38, h * 0.13)], radius=6, fill=(0, 0, 0, 120))
    draw.text((w * 0.08, h * 0.085), badge, fill=(255, 200, 150), anchor='lm', font=font_s)

    img.save(path, 'JPEG', quality=90)


class Command(BaseCommand):
    help = 'Generate local food/cuisine images (works offline on office network)'

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parent.parent.parent.parent / 'static' / 'img'

        for name, color in CUISINE_COLORS.items():
            draw_food_card(
                base / 'cuisines' / f'{name}.jpg',
                name.title(), 'Cuisine', color, CUISINE_EMOJI.get(name, '🍽'), (200, 200),
            )

        draw_food_card(
            base / 'stores' / 'kajal.jpg',
            'Kajal', 'Indian & Biryani', (35, 38, 55), '🏪', (800, 500),
        )

        foods = [
            ('biryani-chicken', 'Chicken Biryani', 'Hyderabadi Style'),
            ('biryani-mutton', 'Mutton Biryani', 'Dum Cooked'),
            ('biryani-veg', 'Veg Biryani', 'Aromatic Basmati'),
            ('biryani-egg', 'Egg Biryani', 'Spiced & Fluffy'),
            ('butter-chicken', 'Butter Chicken', 'Creamy Tomato'),
            ('paneer', 'Paneer Masala', 'Rich & Creamy'),
            ('dal', 'Dal Makhani', 'Slow Cooked'),
            ('tikka', 'Chicken Tikka', 'Tandoor Grilled'),
            ('naan', 'Butter Naan', 'Tandoor Fresh'),
            ('rice', 'Jeera Rice', 'Basmati'),
            ('gulab', 'Gulab Jamun', 'Sweet Classic'),
            ('rasmalai', 'Rasmalai', 'Bengali Sweet'),
            ('kheer', 'Kheer', 'Rice Pudding'),
        ]
        for slug, title, sub in foods:
            color = FOOD_COLORS.get(slug, (252, 128, 25))
            emoji = FOOD_EMOJI.get(slug, '🍽')
            draw_food_card(base / 'foods' / f'{slug}.jpg', title, sub, color, emoji, (400, 300))

        self.stdout.write(self.style.SUCCESS('All local images saved to static/img/ (no internet used)'))
