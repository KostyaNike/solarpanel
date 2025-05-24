from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')

class SolarPanel(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    power = models.CharField(max_length=50)
    size = models.CharField(max_length=100)
    weight = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    full_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title