from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from real_estate.models import Lands, Land_Project
from user.models import Customer, Land_Projet_Tracker_Offer


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name',
                                                 'placeholder': 'Entrez votre prénom : '}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'username',
                                            'placeholder': 'Entrez votre nom d\'utilisateur (Exemple: ibou2241)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name',
                                                'placeholder': 'Entrez votre nom de famille :'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'name': 'email',
                                            'placeholder': 'Entrez votre email :'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'type': 'password',
                                               'placeholder': 'Entrez votre mot de passe :'}),
        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')


#Edit the first name, last name, email and the username
class EditUserInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name',
                                                 'placeholder': 'Entrez votre prénom : '}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'username',
                                            'placeholder': 'Entrez votre nom d\'utilisateur (Exemple: ibou2241)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name',
                                                'placeholder': 'Entrez votre nom de famille :'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'name': 'email',
                                            'placeholder': 'Entrez votre email :'}),
        }

    def clean(self):
        cleaned_data = super(EditUserInfoForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')


#Edit the phone, adress, country, avatar and the birthdate
class EditUserInfoForm1(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'phone', 'adress', 'country', 'birth_date'
        ]


class EditUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = [
            'old_password', 'new_password1', 'new_password2'
        ]
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'old_password', 'type': 'password',
                                               'placeholder': 'Entrez votre actuel mot de passe :'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'new_password1', 'type': 'password',
                                                   'placeholder': 'Entrez votre nouveau mot de passe :'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'new_password2', 'type': 'password',
                                                   'placeholder': 'Entrez a nouveau votre nouveau mot de passe :'}),
        }

    def clean(self):
        cleaned_data = super(EditUserPasswordForm, self).clean()
        password = cleaned_data.get('password')


class Land_Form(forms.ModelForm):
    class Meta:
        model = Lands
        fields = [
            'region', 'adress', 'area', 'additional_info', 'price', 'minimum_price', 'maximum_price'
        ]


class Land_Project_Form(forms.ModelForm):
    class Meta:
        model = Land_Project
        fields = [
            'real_estate_project_type', 'land_type', 'service_type'
        ]


class Land_Projet_Tracker_Offer_Form(forms.ModelForm):
    class Meta:
        model = Land_Projet_Tracker_Offer
        fields = [
            'full_name', 'phone_number', 'amount', 'additional_info', 'land_region', 'land_adress', 'land_area',
            'land_price', 'land_plan_situation_id', 'land_paper_type_id', 'user_id', 'accepted'
        ]