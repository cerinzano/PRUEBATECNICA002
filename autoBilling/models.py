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

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

class Job(models.Model):
    id_jwt = models.CharField(max_length=255, primary_key=True)
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    operational_model = models.CharField(max_length=255)
    store_id = models.CharField(max_length=255)
    store_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='jobs')

class StoreAvailable(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Operation(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    stores = models.ManyToManyField(StoreAvailable, related_name='operations')
    options = models.ManyToManyField('Option', related_name='operations')

    def __str__(self):
        return f"Operation {self.id}"

class Option(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    operational_model = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Option {self.id}"

