import hashlib
from django import forms
from .models import User
from django.forms import ModelForm
import joblib
import pandas as pd
from datetime import datetime
import cloudpickle

# from .model_pred import AgeTransformer, BmiTransformer

#region ouverture du modèle

with open('assurance/basic_linreg_model.pkl', 'rb') as file:
    model_pred = cloudpickle.load(file)

#region Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')


#region Formulaire opérateur

class OperateurForm(ModelForm):

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

#region Formulaire client

class ClientForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','sexe','region','statut_fumeur','nombre_enfant','password','email','date_de_naissance','telephone','poids','taille']

    def save(self, commit=True):
        # Récupérer l'instance de l'utilisateur avant d'ajouter le hachage
        user = super().save(commit=False)

        #éviter l'erreur des champs vides
        if user.poids is not None and user.taille is not None:
            if user.poids > 0 and user.taille >0 :
                user.imc = user.poids / ((user.taille /100) ** 2)
        
        # Si le mot de passe a été modifié, hachage avec SHA-256  
        if self.cleaned_data.get('password'):
            password = self.cleaned_data['password']
            user.set_password(password)  # Utilise le hashage sécurisé de Django
            user.age = datetime.now().year - user.date_de_naissance.year
            user.is_client = True      

            # #faire un dataframe pour model
            df_pour_model = pd.DataFrame([[user.age, user.sexe,user.imc,user.nombre_enfant,user.statut_fumeur,user.region]], columns=['age','sex','bmi','children','smoker','region'])
            print(df_pour_model)
            print(df_pour_model.dtypes)

            with open('assurance/basic_linreg_model.pkl', 'rb') as file:
                model_pred = cloudpickle.load(file)
            charge = model_pred.predict(df_pour_model)
            print(charge)
            print(charge[0])
            user.charges = charge[0]

        
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
        fields = ['last_name', 'first_name', 'email', 'telephone', 'date_de_naissance', 'sexe', 'taille', 'poids', 'nombre_enfant', 'statut_fumeur', 'region']

    def save(self, commit=True):
        user = super().save(commit=False)
        # model = joblib.load("prime_assurance/assurance/complete_pipeline.pkl")
        model_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'complete_pipeline.pkl')
        model = joblib.load(model_path)
        df_pour_model = pd.DataFrame([[user.age, user.sexe,user.imc,user.nombre_enfant,user.statut_fumeur,user.region]], columns=['age','sex','bmi','children','smoker','region'])
        user.charge = model.predict(df_pour_model)[0]
        print(user.charge)



class ProspectForm(ClientForm):


    class Meta:
        model = User
        fields = ['first_name','last_name','username','sexe','region','statut_fumeur','nombre_enfant','password','email','date_de_naissance','telephone','poids','taille']

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
            user.age = datetime.now().year - user.date_de_naissance.year
            user.is_prospect = True

            # #faire un dataframe pour model
            df_pour_model = pd.DataFrame([[user.age, user.sexe,user.imc,user.nombre_enfant,user.statut_fumeur,user.region]], columns=['age','sex','bmi','children','smoker','region'])
            charge = model_pred.predict(df_pour_model)
            user.charges = charge[0]
        
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        
        return user




    
