import os
import random
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import time
from django.utils.timezone import now
from datetime import timedelta
from .models import SolarPanel

def index(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'products')
    image_files = []

    if os.path.exists(media_path):
        # Фильтруем только изображения
        image_files = [f"{settings.MEDIA_URL}products/{f}" for f in os.listdir(media_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]

    return render(request, 'solar_main/index.html', {'file_urls': image_files})

TELEGRAM_BOT_TOKEN = '7890565191:AAGwTmdkxe-nCuOpNCAMu5YKVUjKDxl6vOQ'
TELEGRAM_CHAT_ID = '-1002515072654'

@csrf_exempt
def form_page(request):
    cooldown_key = 'last_form_submit'
    cooldown_time = 3600  # 1 час в секундах

    if request.method == 'POST':
        last_submit = request.session.get(cooldown_key)
        current_time = int(time.time())

        if last_submit and current_time - last_submit < cooldown_time:
            wait_min = int((cooldown_time - (current_time - last_submit)) / 60)
            message = f"Ви вже надсилали форму нещодавно. Спробуйте знову через {wait_min} хвилин."
            return render(request, 'solar_main/form.html', {"message": message, "blocked": True})

        # Сохраняем момент отправки
        request.session[cooldown_key] = current_time

        full_name = request.POST.get('full_name', '')
        phone = '+380' + request.POST.get('phone_number', '')
        city = request.POST.get('city', '')
        description = request.POST.get('user_request', '')

        message_text = (
            f"📥 Новий запит з форми:\n\n"
            f"👤 Ім’я: {full_name}\n"
            f"📞 Телефон: {phone}\n"
            f"🏙️ Місто: {city}\n"
            f"📝 Повідомлення: {description}"
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message_text}

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                message = "Форма надіслана успішно, ми зв'яжемося з вами найближчим часом."
            else:
                message = "Помилка відправки в Telegram. Повідомлення не було доставлено."
        except Exception:
            message = "Сталася помилка при надсиланні в Telegram."

        return render(request, 'solar_main/form.html', {"message": message})

    return render(request, 'solar_main/form.html')

PRODUCTS = [
    {
        "id": 1,
        "title": "HS435TC-MHO-D",
        "price": 60.00,
        "power": "435 W",
        "size": "1722×1134×30 mm",
        "weight": "24 kg",
        "description": "Сонячна панель HS435TC-MHO-D — це двосторонній модуль з високою ефективністю та довговічністю.",
        "image": "products/hs435.jpg"
    },
    {
        "id": 2,
        "title": "HS450TC-MHC-D",
        "price": 64.00,
        "power": "450 W",
        "size": "1762×1134×30 mm",
        "weight": "24.5 kg",
        "description": "Потужна модель з покращеними характеристиками для комерційного використання.",
        "image": "products/hs450.jpg"
    },
    {
        "id": 3,
        "title": "HS580TC-MHO-D",
        "price": 78.00,
        "power": "580 W",
        "size": "2279×1134×30 mm",
        "weight": "31.5 kg",
        "description": "Максимальна продуктивність з найвищою якістю матеріалів.",
        "image": "products/hs580.jpg"
    },
    {
        "id": 4,
        "title": "HS620TC-MHC-D",
        "price": 83.00,
        "power": "620 W",
        "size": "2382×1134×30 mm",
        "weight": "33.7 kg",
        "description": "Ідеальний вибір для великомасштабних проектів.",
        "image": "products/hs620.jpg"
    }
]

def products_page(request):
    products = SolarPanel.objects.all()
    return render(request, 'solar_main/products.html', {'products': products})

def product_detail(request, product_id):
    try:
        panel = SolarPanel.objects.get(id=product_id)
    except SolarPanel.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'solar_main/product_detail.html', {'panel': panel})
