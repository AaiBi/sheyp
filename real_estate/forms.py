from django import forms
from real_estate.models import Property, Lands, Land_Images1, Apartment, Apartment_Image, Studio_Image, Studio, \
    House_Image, House, Room, Room_Image
from user.models import Cart


class Property_Form(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'region'
        ]


class Apartment_Form(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'adress', 'floor_level', 'area', 'aditionnal_info', 'number_living_room', 'number_shared_bathroom',
            'number_kitchen', 'closette', 'number_bedroom_with_private_bathroom', 'number_bedroom_without_bathroom',
            'terace', 'balcony', 'rent_price', 'sale_price', 'minimum_price', 'maximum_price'
        ]


class Apartment_Image_Form(forms.ModelForm):
    class Meta:
        model = Apartment_Image
        fields = ['image']


class Studio_Form(forms.ModelForm):
    class Meta:
        model = Studio
        fields = [
            'adress', 'floor_level', 'area', 'aditionnal_info', 'closette',
            'terace', 'balcony', 'rent_price', 'sale_price', 'minimum_price', 'maximum_price'
        ]


class Studio_Image_Form(forms.ModelForm):
    class Meta:
        model = Studio_Image
        fields = ['image']


class House_Form(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'adress', 'area', 'aditionnal_info', 'number_shared_bathroom', 'number_living_room',
            'number_private_bathroom', 'number_bedroom', 'number_kitchen', 'closette',
            'terace', 'garage', 'rent_price', 'sale_price', 'minimum_price', 'maximum_price'
        ]


class House_Image_Form(forms.ModelForm):
    class Meta:
        model = House_Image
        fields = ['image']


class Room_Form(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'adress', 'private_bathroom', 'shared_bathroom', 'shared_kitchen', 'shared_closette',
            'area', 'rent_price', 'minimum_rent_price', 'maximum_rent_price', 'aditionnal_info'
        ]


class Room_Image_Form(forms.ModelForm):
    class Meta:
        model = Room_Image
        fields = ['image']





class Land_Form(forms.ModelForm):
    class Meta:
        model = Lands
        fields = [
            'region', 'adress', 'area', 'additional_info', 'price', 'minimum_price', 'maximum_price'
        ]


class Land_Images1_Form(forms.ModelForm):
    class Meta:
        model = Land_Images1
        fields = [
            'image'
        ]


class Cart_Form(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [
            'land_id', 'property_id'
        ]