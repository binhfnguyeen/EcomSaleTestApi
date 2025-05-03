#!/bin/bash

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Thu thập static files
python manage.py collectstatic --noinput

# Áp dụng migrate
python manage.py migrate --noinput

# Tạo superuser nếu chưa tồn tại
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Admin@123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
END