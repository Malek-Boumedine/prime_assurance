import hashlib
from django import forms
from .models import User
from django.forms import ModelForm, Form
import joblib


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')


class OperateurForm(ModelForm):
    sexe = forms.ChoiceField(
        choices=[('male', 'Homme'), ('female', 'Femme')],
        widget=forms.RadioSelect
        # required=False 
    )
    poste = forms.ChoiceField(
    choices=[('courtier', 'Courtier'), ('manager', 'Manager')],
    widget=forms.RadioSelect,
    required=False
    )

    # is_operateur = forms.ChoiceField(
    #     choices=[(0, 'Non'), (1, 'Oui')],
    #     widget=forms.RadioSelect,
    #     required=False
    # )

    # is_client = forms.ChoiceField(
    #     choices=[(0, 'Non'), (1, 'Oui')],
    #     widget=forms.RadioSelect,
    #     required=False
    # )
    # is_prospect = forms.ChoiceField(
    #     choices=[(0, 'Non'), (1, 'Oui')],
    #     widget=forms.RadioSelect,
    #     required=False
    # )

    class Meta:
        model = User
        fields = ['first_name','last_name','sexe','username','password','email','date_de_naissance','telephone','anciennete','poste']


    def save(self, commit=True):
        # Récupérer l'instance de l'utilisateur avant d'ajouter le hachage
        user = super().save(commit=False)
        
        # Si le mot de passe a été modifié, hachage avec SHA-256
        if self.cleaned_data.get('password'):
            password = self.cleaned_data['password']
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user.password = hashed_password
        
        user.is_operateur = True
        
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        
        return user

class ClientForm(ModelForm):
    
    sexe = forms.ChoiceField(
        choices=[('male', 'Homme'), ('female', 'Femme')],
        widget=forms.RadioSelect,
        required=False 
    )

    region = forms.ChoiceField(
        choices=[('northest', 'Northest'), ('northeast', 'Northeast'),
                 ('southest', 'Southest'), ('southeast', 'Southeast')],
        widget=forms.RadioSelect,
        required=False
    )

    statut_fumeur = forms.ChoiceField(
        choices=[('yes', 'oui'), ('no', 'Non')],
        widget=forms.RadioSelect,
        required=False
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password','email','date_de_naissance','telephone', 'taille', 'poids']

    def save(self, commit=True):
        # Récupérer l'instance de l'utilisateur avant d'ajouter le hachage
        user = super().save(commit=False)

        #éviter l'erreur des champs vides
        if user.poids is not None and user.taille is not None:
            if user.poids > 0 and user.taille >0 :
                user.imc = user.poids / ((user.taille /100) ** 2)
        
        # Si le mot de passe a été modifié, hachage avec SHA-256        
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Utilise le hashage natif de Django
            user.is_client = False
        
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        
        return user

from django.conf import settings
import joblib
import pandas as pd
import os


class DevisForm(ClientForm):
    class Meta(ClientForm.Meta):
        model = User
        fields = ['last_name', 'first_name', 'email', 'telephone', 'date_de_naissance', 'sexe', 'taille', 'poids', 'nombre_enfants', 'statut_fumeur', 'region']

    def save(self, commit=True):
        user = super().save(commit=False)
        # model = joblib.load("prime_assurance/assurance/complete_pipeline.pkl")
        model_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'complete_pipeline.pkl')
        model = joblib.load(model_path)
        df_pour_model = pd.DataFrame([[user.age, user.sexe,user.imc,user.nombre_enfant,user.statut_fumeur,user.region]], columns=['age','sex','bmi','children','smoker','region'])
        user.charge = model.predict(df_pour_model)[0]
        print(user.charge)



class ProspectForm(ClientForm):

    def save(self, commit=True):
        # Récupérer l'instance de l'utilisateur avant d'ajouter le hachage
        user = super().save(commit=False)

        #éviter l'erreur des champs vides
        if user.poids > 0 and user.taille >0 :
            user.imc = user.poids / ((user.taille /100) ** 2)
        
        # Si le mot de passe a été modifié, hachage avec SHA-256
        if self.cleaned_data.get('password'):
            password = self.cleaned_data['password']
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user.password = hashed_password
            user.is_client = False
            user.is_prospect = True
        
        
        
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
    
