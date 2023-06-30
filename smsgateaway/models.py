from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)

class Carrier(models.Model):
    name = models.CharField(max_length=255)
    phone_numbers = models.ManyToManyField(PhoneNumber)

    