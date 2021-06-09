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
    medical_id = models.CharField(max_length=20, blank=True, null=True)
    # puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
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
    area = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    class_type = models.CharField(max_length=1, default="Z")
    bed_availability = models.IntegerField(default=0)
    image_name = models.CharField(max_length=200, default="default.img")

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100, default="-")
    jenis_pengobatan = models.CharField(max_length=30, default="-")
    start_time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    prediction_time = models.IntegerField(default=0)
    painscale = models.IntegerField(default=1) # 1=painless, 2=pain, 3=very-pain
    immediacy = models.IntegerField(default=5) # 1=immediate, 2=emergent, 3=urgent, 4=semi-urgent, 5=nonurgent
    temperature = models.IntegerField(default=1) # 1=normal, #warm

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100, null=True, blank=True)
    drug_list = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True, default=timezone.now)

class BannerHeader(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)

class CovidData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=timezone.now)
    cases = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    death = models.IntegerField(default=0)
