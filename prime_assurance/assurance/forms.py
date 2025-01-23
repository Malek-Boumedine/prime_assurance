from django import forms
import hashlib
from .models import User # Opérateur, Client, Prospect
from django.forms import ModelForm, Form

# class OperateurFrom(ModelForm):
#     class Meta:


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

    villes = forms.ChoiceField(
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
        fields = ['first_name','last_name','username','password','email','date_de_naissance','telephone','poids','taille']

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
            user.is_client = True
        
        
        
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        
        return user

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
    
