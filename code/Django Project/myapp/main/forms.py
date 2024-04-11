# main/forms.py
from django import forms
from .models import MissingPerson


class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = '__all__'


