from django.contrib import admin
from construction.models import Construction_Project, Construction_Type, Construction_floor, Quote_Project, \
    Quote_Project_Step, Quote_Project_Ouvrage, Quote_Project_Materiaux, Mesure_Unit, Materiaux, Country

admin.site.register(Construction_Project)
admin.site.register(Construction_floor)
admin.site.register(Construction_Type)

admin.site.register(Quote_Project)
admin.site.register(Quote_Project_Step)
admin.site.register(Quote_Project_Ouvrage)
admin.site.register(Quote_Project_Materiaux)
admin.site.register(Mesure_Unit)
admin.site.register(Materiaux)
admin.site.register(Country)
