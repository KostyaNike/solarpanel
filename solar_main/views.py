import os
import random
from django.conf import settings
from django.shortcuts import render

def index(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'products')
    image_files = []

    if os.path.exists(media_path):
        # Фильтруем только изображения
        image_files = [f"{settings.MEDIA_URL}products/{f}" for f in os.listdir(media_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]

    return render(request, 'solar_main/index.html', {'file_urls': image_files})