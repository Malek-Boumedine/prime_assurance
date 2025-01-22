from django import forms
from .models import Operateur#, Client, Prospect
from django.forms import ModelForm

class OperateurFrom(ModelForm):
    class Meta:
        model = Operateur
        fields = ['nom','prenom','email','date_de_naissance','telephone','anciennete','poste']

