import hashlib
from django import forms
from .models import User, RendezVous
from django.forms import ModelForm
import joblib
import pandas as pd
from datetime import datetime
import cloudpickle
from django.conf import settings
import os




with open('assurance/basic_linreg_model.pkl', 'rb') as file:
    model_pred = cloudpickle.load(file)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')
    

class RendezVousForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    heure = forms.ChoiceField(choices=[
        ('09:00', '09:00 - 09:30'),
        ('09:30', '09:30 - 10:00'),
        ('10:00', '10:00 - 10:30'),
        ('10:30', '10:30 - 11:00'),
        ('11:00', '11:00 - 11:30'),
        ('11:30', '11:30 - 12:00'),
        ('14:00', '14:00 - 14:30'),
        ('14:30', '14:30 - 15:00'),
        ('15:00', '15:00 - 15:30'),
        ('15:30', '15:30 - 16:00'),
        ('16:00', '16:00 - 16:30'),
        ('16:30', '16:30 - 17:00'),
        ('17:00', '17:00 - 17:30'),
        ('17:30', '17:30 - 18:00'),
    ])    
    
    class Meta:
        model = RendezVous
        fields = ['nom', 'prenom', 'motif', 'operateur', 'type']
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        heure = cleaned_data.get('heure')
        operateur = cleaned_data.get('operateur')
        
        if date and heure and operateur:
            heure_obj = datetime.strptime(heure, '%H:%M').time()
            date_heure = datetime.combine(date, heure_obj)

            # Vérifier si un rendez-vous existe déjà
            if RendezVous.objects.filter(operateur=operateur, date_heure=date_heure).exists():
                raise forms.ValidationError("Ce créneau est déjà pris pour cet opérateur. Veuillez choisir un autre horaire.")

            cleaned_data['date_heure'] = date_heure
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        date = self.cleaned_data.get('date')
        heure = self.cleaned_data.get('heure')
        if date and heure:
            heure_obj = datetime.strptime(heure, '%H:%M').time()
            instance.date_heure = datetime.combine(date, heure_obj)
        if commit:
            instance.save()
        return instance    


class OperateurForm(ModelForm):

    sexe = forms.ChoiceField(required=True, choices=[('male', 'Homme'), ('female', 'Femme')])
    region = forms.ChoiceField(required=True, choices=[('northwest', 'Northwest'), ('northeast', 'Northeast'), ('southwest', 'Southwest'), ('southeast', 'Southeast')])
    poste = forms.ChoiceField(required=True, choices=[('courtier', 'Courtier'), ('manager', 'Manager')])

    class Meta:
        model = User
        fields = ['first_name','last_name','sexe','username','password','email','date_de_naissance','telephone','anciennete','poste']
        widgets = {
            'date_de_naissance': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})
        }

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


class ModifierProfilForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','sexe','region','statut_fumeur','nombre_enfant','email','date_de_naissance','telephone','poids','taille']

class OperateurModification(ModelForm):

    model = User
    fields = ['first_name','last_name','sexe','username','email','date_de_naissance','telephone','poste']
    widgets = {
        'date_de_naissance': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})
    }
    


    

class ClientForm(ModelForm):
    sexe = forms.ChoiceField(required=True, choices=[('male', 'Homme'), ('female', 'Femme')])
    region = forms.ChoiceField(required=True, choices=[('northwest', 'Northwest'), ('northeast', 'Northeast'), ('southwest', 'Southwest'), ('southeast', 'Southeast')])
    statut_fumeur = forms.ChoiceField(choices=[('yes', 'Oui'), ('no', 'Non')])
    first_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirmer le mot de passe')

    class Meta:
        model = User
        fields = ['first_name','last_name','username','sexe','region','statut_fumeur','nombre_enfant','password','confirm_password','email','date_de_naissance','telephone','poids','taille']
        widgets = {
            'date_de_naissance': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})
            
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return cleaned_data

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
            user.is_prospect = False

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
    

class DevisForm(ClientForm):
    password = None
    confirm_password = None
    class Meta(ClientForm.Meta):
        model = User
        fields = ['last_name', 'first_name', 'email', 'telephone', 'date_de_naissance', 'sexe', 'taille', 'poids', 'nombre_enfant', 'statut_fumeur', 'region']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'})
        }

    def calculer(self):
        user = super().save(commit=False)

        if user.poids and user.taille:
            user.imc = user.poids / ((user.taille/100) ** 2)
            
        if user.date_de_naissance:
            user.age = datetime.now().year - user.date_de_naissance.year
        
        df_pour_model = pd.DataFrame([[user.age, user.sexe, user.imc, user.nombre_enfant, user.statut_fumeur, user.region]], columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])

        try:
            with open('assurance/basic_linreg_model.pkl', 'rb') as file:
                model = cloudpickle.load(file)
            montant = model.predict(df_pour_model)[0]
            return montant
        except Exception as e:
            print(f"Erreur lors du calcul : {e}")
            return None


class ProspectForm(ClientForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','sexe','region','statut_fumeur','nombre_enfant','password','email','date_de_naissance','telephone','poids','taille']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'})
        }

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
    




    
