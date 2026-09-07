# Gajal Food — Online Food Ordering Platform

Django-based food delivery app with merchant, customer, and admin roles.

## Features

- Multi-role auth (Admin, Merchant, Customer)
- Email OTP signup & password reset (Gmail SMTP)
- Merchant store & menu management
- Customer cart, checkout & dummy payments (GPay, PhonePe, Card)
- Swiggy-inspired UI with geolocation
- SQLite (local) / PostgreSQL (production)

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # Edit with your secrets
python manage.py migrate
python manage.py generate_images
python manage.py seed_kajal
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

**Demo merchant:** `kajal` / `Kajal@123`

## Environment Variables

See `.env.example` for all settings. Never commit `.env`.

## EC2 Deployment

See [DEPLOY.md](DEPLOY.md) for full AWS EC2 setup with Nginx + Gunicorn.

## Tech Stack

- Django 5.2
- Bootstrap 5
- SQLite / PostgreSQL
- Gmail SMTP

## License

MIT
