from django.contrib.auth.models import User
from django.db import models


class contact_message(models.Model):
    full_name = models.CharField(max_length=500)
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return self.subject


class Provider(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField()
    materials_supplied_list = models.TextField()
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    adress = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class Notation_System(models.Model):
    name = models.CharField(max_length=500)
    stars = models.IntegerField()
    country = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Success_Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    land_project_id = models.IntegerField(default=0)
    property_project_id = models.IntegerField(default=0)
    construction_project_id = models.IntegerField(default=0)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stars
