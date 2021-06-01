from django.db import models
from django.utils import timezone

import uuid

# Create your models here.
class Puskesmas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=13)
    bpjs_number = models.CharField(max_length=15)
    identity_number = models.CharField(max_length=20)
    sex = models.CharField(max_length=10)
    age = models.IntegerField(default=0)

class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    jenis_pengobatan = models.CharField(max_length=30)
    start_time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

class CovidData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    cases = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    death = models.IntegerField(default=0)