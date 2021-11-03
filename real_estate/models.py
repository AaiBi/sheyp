from django.db import models
from django.contrib.auth.models import User


class Real_Estate_Projet_Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return self.name

                                ##Property Management part##


class Service_Type(models.Model):
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Land_Paper_Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Property_Type(models.Model):
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Property(models.Model):
    region = models.CharField(max_length=200, default="")
    created = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(default=1) #1 mean active #0 cancelled
    done = models.BooleanField(default=0)
    service_type = models.ForeignKey(Service_Type, on_delete=models.CASCADE)
    property_type = models.ForeignKey(Property_Type, on_delete=models.CASCADE)
    real_estate_project_type = models.ForeignKey(Real_Estate_Projet_Type, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Apartment(models.Model):
    adress = models.CharField(max_length=200, default="")
    floor_level = models.IntegerField()
    area = models.IntegerField(default=0)
    aditionnal_info = models.TextField(blank=True, default="")
    number_bedroom_with_private_bathroom = models.IntegerField(default=0)
    number_bedroom_without_bathroom = models.IntegerField(default=0)
    number_shared_bathroom = models.IntegerField(default=0)
    number_living_room = models.IntegerField(default=0)
    number_kitchen = models.IntegerField(default=0)
    closette = models.CharField(max_length=5, default="")
    terace = models.CharField(max_length=5, default="")
    balcony = models.CharField(max_length=5, default="")
    rent_price = models.IntegerField(blank=True, default=0)
    sale_price = models.IntegerField(blank=True, default=0)
    minimum_price = models.IntegerField(blank=True, default=0)
    maximum_price = models.IntegerField(blank=True, default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, default="")


class Apartment_Image(models.Model):
    image = models.ImageField(upload_to='real_estate/images/apartment/', blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, default="")


class Studio(models.Model):
    adress = models.CharField(max_length=200, default="")
    floor_level = models.IntegerField()
    area = models.IntegerField()
    aditionnal_info = models.TextField(blank=True)

    closette = models.CharField(max_length=5, default="")
    terace = models.CharField(max_length=5, default="")
    balcony = models.CharField(max_length=5, default="")
    rent_price = models.IntegerField(blank=True, default=0)
    sale_price = models.IntegerField(blank=True, default=0)
    minimum_price = models.IntegerField(blank=True, default=0)
    maximum_price = models.IntegerField(blank=True, default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, default="")


class Studio_Image(models.Model):
    image = models.ImageField(upload_to='real_estate/images/studio/', blank=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, blank=True, default="")


class House(models.Model):
    adress = models.CharField(max_length=200, default="")
    number_shared_bathroom = models.IntegerField()
    number_private_bathroom = models.IntegerField(default=0)
    number_living_room = models.IntegerField(default=0)
    number_bedroom = models.IntegerField(default=0)
    number_kitchen = models.IntegerField(default=0)
    area = models.IntegerField()

    closette = models.CharField(max_length=5, default="")
    garage = models.CharField(max_length=5, default="")
    aditionnal_info = models.TextField(blank=True)
    terace = models.CharField(max_length=5, default="")
    rent_price = models.IntegerField(blank=True, default=0)
    sale_price = models.IntegerField(blank=True, default=0)
    minimum_price = models.IntegerField(blank=True, default=0)
    maximum_price = models.IntegerField(blank=True, default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, default="")


class House_Image(models.Model):
    image = models.ImageField(upload_to='real_estate/images/house/', blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, default="")


class Room(models.Model):
    adress = models.CharField(max_length=200, default="")
    private_bathroom = models.CharField(max_length=5, default="")
    shared_bathroom = models.CharField(max_length=5, default="")
    shared_kitchen = models.CharField(max_length=5, default="")
    shared_closette = models.CharField(max_length=5, default="")
    area = models.IntegerField(default=0)
    rent_price = models.IntegerField(blank=True, default=0)
    minimum_rent_price = models.IntegerField(blank=True, default=0)
    maximum_rent_price = models.IntegerField(blank=True, default=0)
    aditionnal_info = models.TextField(blank=True, default="")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, default="")


class Room_Image(models.Model):
    image = models.ImageField(upload_to='real_estate/images/room/', blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, default="")
                                        ##End Property Management part##

                                        ##Land part##


class Land_Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Land_Plan_Situation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Land_Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=15, default="In progress") #the statut can be 'in progress', or 'Done'
    accepted = models.BooleanField(default=0) #the statut can be 'accepted = 1', or 'not accepted=0'
    done = models.BooleanField(default=0)
    real_estate_project_type = models.ForeignKey(Real_Estate_Projet_Type, on_delete=models.CASCADE, default="")
    land_type = models.ForeignKey(Land_Type, on_delete=models.CASCADE, default="")
    service_type = models.ForeignKey(Service_Type, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")


class Lands(models.Model):
    region = models.CharField(max_length=200, default="")
    adress = models.CharField(max_length=200, default="0")
    area = models.IntegerField(default="0")
    additional_info = models.TextField(blank=True, default="0")
    price = models.CharField(max_length=100, default=0)
    minimum_price = models.CharField(max_length=100, default="0")
    maximum_price = models.CharField(max_length=100, default="0")
    land_plan_situation = models.ForeignKey(Land_Plan_Situation, on_delete=models.CASCADE, default="")
    land_paper_type = models.ForeignKey(Land_Paper_Type, on_delete=models.CASCADE, blank=True, default="")
    land_project = models.ForeignKey(Land_Project, on_delete=models.CASCADE, default="")


class Land_Propostion(models.Model):
    location = models.CharField(max_length=200, blank=True, default="0")
    area = models.IntegerField(blank=True, default="0")
    land_plan_situation = models.CharField(max_length=100, blank=True, default="0")
    additional_info = models.TextField(blank=True, default="0")
    price = models.CharField(max_length=100, default="0")
    date = models.DateTimeField(auto_now_add=True)
    land_info = models.ForeignKey(Lands, on_delete=models.CASCADE)


class Land_Images1(models.Model):
    image = models.ImageField(upload_to='real_estate/images/land/', blank=True, default="")
    land = models.ForeignKey(Lands, on_delete=models.CASCADE, default="")


class Land_Images2(models.Model):
    image = models.ImageField(upload_to='real_estate/images/', blank=True)
    land_proposition = models.ForeignKey(Land_Propostion, on_delete=models.CASCADE, default="")


class Land_Purchase_Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    land_info = models.ForeignKey(Lands, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

                                    ##End land part##