from django import forms
from construction.models import Construction_Project, Construction_floor


class Construction_Project_Form(forms.ModelForm):
    class Meta:
        model = Construction_Project
        fields = [
            'region', 'adress', 'area', 'area_usable', 'aditionnal_info', 'number_floor',
            'client_first_name', 'client_last_name', 'client_email',
            'client_phone_number'
        ]


class Construction_floor_Form(forms.ModelForm):
    class Meta:
        model = Construction_floor
        fields = [
            'floor_level', 'aditionnal_info', 'number_bedroom_with_bathroom', 'number_bedroom_without_bathroom',
            'number_shared_bathroom', 'garage', 'number_living_room', 'number_kitchen', 'closette', 'terace',
            'balcony'
        ]