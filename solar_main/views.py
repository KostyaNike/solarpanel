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