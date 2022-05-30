from django.db import models
from django.contrib.auth.models import User


class Construction_Type(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Construction_Project(models.Model):
    region = models.CharField(max_length=200, default="")
    adress = models.CharField(max_length=200, default="0")
    area = models.IntegerField(default="0")
    area_usable = models.IntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=15, default="In progress")  # the statut can be 'In progress', 'Done' or 'Paused'
    accepted = models.BooleanField(default=0)  # the statut can be 'accepted = 1', or 'not accepted=0'
    aditionnal_info = models.TextField(blank=True)
    number_floor = models.IntegerField(blank=True)
    client_first_name = models.CharField(max_length=300, default="")
    client_last_name = models.CharField(max_length=300, default="")
    client_email = models.CharField(max_length=300, default="")
    client_phone_number = models.CharField(max_length=30, default="")
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    construction_type = models.ForeignKey(Construction_Type, on_delete=models.CASCADE, default="")


class Construction_floor(models.Model):
    floor_level = models.IntegerField()
    aditionnal_info = models.TextField(blank=True, default="")
    number_bedroom_with_bathroom = models.IntegerField(default=0)
    number_bedroom_without_bathroom = models.IntegerField(default=0)
    number_shared_bathroom = models.IntegerField()
    garage = models.CharField(max_length=5, default="No")
    number_living_room = models.IntegerField(default=0)
    number_kitchen = models.IntegerField(default=0)
    closette = models.CharField(max_length=5, default="No")
    terace = models.CharField(max_length=5, default="No")
    balcony = models.CharField(max_length=5, default="No")
    construction_project = models.ForeignKey(Construction_Project, on_delete=models.CASCADE)