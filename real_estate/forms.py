from django import forms
from real_estate.models import Property, Lands, Land_Images1, Property_Type_Details, Property_Type_Details_Image
from user.models import Cart


class Property_Form(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'region', 'ref'
        ]


class Property_Type_Detail_Form(forms.ModelForm):
    class Meta:
        model = Property_Type_Details
        fields = [
            'adress', 'floor_level', 'area', 'aditionnal_info', 'number_bedroom_with_private_bathroom', 'number_bedroom_without_bathroom',
            'number_shared_bathroom', 'number_living_room', 'number_kitchen', 'closette', 'garage',
            'terace', 'balcony', 'rent_price', 'sale_price', 'minimum_price', 'maximum_price', 'number_apartment'
        ]


class Property_Type_Detail_Image_Form(forms.ModelForm):
    class Meta:
        model = Property_Type_Details_Image
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