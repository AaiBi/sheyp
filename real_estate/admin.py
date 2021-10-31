from django.contrib import admin
from real_estate.models import Land_Project, Lands, Land_Propostion, Land_Images1, Property_Type, Service_Type, \
    Apartment, Room, Property, Land_Images2, Land_Type, Land_Plan_Situation, Land_Purchase_Order, \
    Real_Estate_Projet_Type, Studio, Studio_Image, House, House_Image, Room_Image, \
    Land_Paper_Type, Apartment_Image

admin.site.register(Real_Estate_Projet_Type)

#land part
admin.site.register(Land_Project)
admin.site.register(Lands)
admin.site.register(Land_Propostion)
admin.site.register(Land_Images1)
admin.site.register(Land_Images2)
admin.site.register(Land_Type)
admin.site.register(Land_Plan_Situation)
admin.site.register(Land_Purchase_Order)

#property purchase,sale or location part
admin.site.register(Property_Type)
admin.site.register(Service_Type)
admin.site.register(Apartment)
admin.site.register(Room)
admin.site.register(Property)
admin.site.register(Studio)
admin.site.register(Studio_Image)
admin.site.register(House)
admin.site.register(House_Image)
admin.site.register(Room_Image)
admin.site.register(Land_Paper_Type)
admin.site.register(Apartment_Image)
