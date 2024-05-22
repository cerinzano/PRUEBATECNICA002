import random
import string
import uuid
from django.db import models

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=50)  # Campo nuevo
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)  # Corregido el duplicado
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name


class Persona(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=50)  # Campo nuevo
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)  # Corregido el duplicado
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
class Product(models.Model):
    id_item = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    photo_url = models.CharField(max_length=200)
    unit = models.CharField(max_length=10)
    sub_unit = models.CharField(max_length=10)
    quantity = models.IntegerField()
    sub_quantity = models.IntegerField()
    weight = models.IntegerField()
    volume = models.IntegerField()
    price = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return self.name

class Operation(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Operation {self.id}"

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    id_job = models.CharField(max_length=1000)
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    operational_model = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    store_id = models.CharField(max_length=255)
    store_name = models.CharField(max_length=255)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return f"Job {self.id}"

