from django import forms

from base_app.models import Notation_System


class Notation_System_Form(forms.ModelForm):
    class Meta:
        model = Notation_System
        fields = [
            'name', 'stars', 'country', 'message'
        ]