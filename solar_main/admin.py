from django.contrib import admin
from .models import Task, SolarPanel

admin.site.register(Task)
@admin.register(SolarPanel)
class SolarPanelAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'power', 'size')
    search_fields = ('title',)
    list_filter = ('power',)
    fields = (
        'title', 'price', 'power', 'size', 'weight',
        'image', 'description', 'full_description'  # ← показываем в форме
    )