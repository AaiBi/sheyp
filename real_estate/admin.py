from django.contrib import admin
from real_estate.models import Land_Project, Lands, Land_Propostion, Land_Images1, Property_Type, Service_Type, \
    Property_Type_Details, Property_Type_Details_Image, Property, Land_Images2, Land_Type, Land_Plan_Situation, Land_Purchase_Order, \
    Real_Estate_Projet_Type, Land_Paper_Type

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
admin.site.register(Property_Type_Details)
admin.site.register(Property_Type_Details_Image)
admin.site.register(Property)
admin.site.register(Land_Paper_Type)
