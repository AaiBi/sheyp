from django.contrib import admin
from construction.models import Construction_Project, Construction_Type, Construction_floor

admin.site.register(Construction_Project)
admin.site.register(Construction_floor)
admin.site.register(Construction_Type)
