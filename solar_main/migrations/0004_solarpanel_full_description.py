# Generated by Django 5.2 on 2025-05-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solar_main', '0003_solarpanel'),
    ]

    operations = [
        migrations.AddField(
            model_name='solarpanel',
            name='full_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
