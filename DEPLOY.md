# Deploy Gajal Food on AWS EC2

## Prerequisites

- AWS account with EC2 access
- GitHub repo: https://github.com/Gajanan180/Gajal
- Domain (optional) or use EC2 public IP

---

## Step 1 — Launch EC2 Instance

1. AWS Console → **EC2** → **Launch Instance**
2. **Name:** gajal-food
3. **AMI:** Ubuntu 22.04 LTS
4. **Instance type:** t2.micro or t3.micro (Free Tier)
5. **Key pair:** Create/download `.pem` file
6. **Security Group — open ports:**
   | Port | Purpose |
   |------|---------|
   | 22   | SSH |
   | 80   | HTTP |
   | 443  | HTTPS (optional) |
7. Launch instance → copy **Public IPv4**

---

## Step 2 — Connect via SSH

```bash
ssh -i "your-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## Step 3 — Install Dependencies on EC2

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git

# Optional: PostgreSQL (recommended for production)
sudo apt install -y postgresql postgresql-contrib
```

---

## Step 4 — Clone Project

```bash
cd /home/ubuntu
git clone https://github.com/Gajanan180/Gajal.git
cd Gajal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

---

## Step 5 — Configure Environment

```bash
nano .env
```

```env
SECRET_KEY=generate-a-long-random-string-here
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_IP,yourdomain.com

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your@gmail.com
```

Replace `YOUR_EC2_IP` with your actual IP (e.g. `3.110.45.12`).

---

## Step 6 — Django Setup

```bash
source venv/bin/activate
python manage.py migrate
python manage.py generate_images
python manage.py seed_kajal
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## Step 7 — Gunicorn Systemd Service

```bash
sudo nano /etc/systemd/system/gajal.service
```

```ini
[Unit]
Description=Gajal Food Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Gajal
Environment="PATH=/home/ubuntu/Gajal/venv/bin"
ExecStart=/home/ubuntu/Gajal/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/Gajal/gajal.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gajal
sudo systemctl enable gajal
sudo systemctl status gajal
```

---

## Step 8 — Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/gajal
```

```nginx
server {
    listen 80;
    server_name YOUR_EC2_IP yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/Gajal/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/Gajal/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/Gajal/gajal.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/gajal /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 9 — Open in Browser

Visit: `http://YOUR_EC2_PUBLIC_IP`

---

## Step 9b — PostgreSQL (Optional, Production)

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE gajal_food;
CREATE USER gajal_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE gajal_food TO gajal_user;
\q
```

Update `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gajal_food
DB_USER=gajal_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=5432
```

Install driver: `pip install psycopg2-binary` (add to requirements.txt)

Then: `python manage.py migrate`

---

## Step 10 — SSL with Let's Encrypt (Optional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Updating After Code Changes

```bash
cd /home/ubuntu/Gajal
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gajal
```

---

## Billing Safety

- Set AWS **Budget Alert** at $5–10
- **Stop** EC2 when not using (don't leave running 24/7 for study)
- Use **t2.micro** Free Tier instance

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 502 Bad Gateway | `sudo systemctl status gajal` — check gunicorn |
| Static files missing | Run `collectstatic` again |
| DisallowedHost | Add EC2 IP to `ALLOWED_HOSTS` in `.env` |
| Email not sending | Check Gmail App Password in `.env` |
