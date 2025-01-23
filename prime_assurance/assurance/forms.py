from django import forms
from .models import User
from django.forms import ModelForm

# class OperateurFrom(ModelForm):
#     class Meta:
#         model = Operateur
#         fields = ['nom','prenom','email','date_de_naissance','telephone','anciennete','poste']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')