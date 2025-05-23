# Generated by Django 5.2 on 2025-05-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solar_main', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarPanel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('power', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=100)),
                ('weight', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='products/')),
                ('description', models.TextField()),
            ],
        ),
    ]
