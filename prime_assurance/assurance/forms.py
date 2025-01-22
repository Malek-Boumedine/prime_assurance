from django import forms
import hashlib
from .models import User # Opérateur, Client, Prospect
from django.forms import ModelForm, Form

# class OperateurFrom(ModelForm):
#     class Meta:


class OperateurForm(ModelForm):
    sexe = forms.MultipleChoiceField(
        choices=[('male', 'Homme'), ('female', 'Femme')],
        widget=forms.RadioSelect,
        required=False 
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
    is_operateur = 1
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
        fields = ['first_name','last_name','sexe','username','password','email','date_de_naissance','telephone','anciennete','poste', 'is_operateur']


    def save(self, commit=True):
        # Récupérer l'instance de l'utilisateur avant d'ajouter le hachage
        user = super().save(commit=False)
        
        # Si le mot de passe a été modifié, hachage avec SHA-256
        if self.cleaned_data.get('password'):
            password = self.cleaned_data['password']
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user.password = hashed_password
        
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        
        return user

class ClientFrom(ModelForm):

    sexe = forms.MultipleChoiceField(
        choices=[('male', 'Homme'), ('female', 'Femme')],
        widget=forms.RadioSelect,
        required=False 
    )

    villes = forms.MultipleChoiceField(
        choices=[('northest', 'Northest'), ('northeast', 'Northeast'),
                 ('southest', 'Southest'), ('southeast', 'Southeast')],
        widget=forms.RadioSelect,
        required=False
    )

    fumeur = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        required=False
    )

    is_client = 1

    class Meta:
        model = User
        fields = ['nom','prenom','email','date_de_naissance','telephone','poids','taille','sexe',"IMC",'status_fumeur','is_client']


    def clean(self):
        cleaned_data = super().clean()

        poids = cleaned_data.get("poids")
        taille = cleaned_data.get("taille")

        # Calcul de l'IMC uniquement si les deux valeurs sont présentes
        if poids and taille:
            try:
                # Assurez-vous que la taille est en mètres et le poids en kilogrammes
                imc = poids / (taille ** 2)
                cleaned_data["IMC"] = round(imc, 0)  # Arrondi de l'IMC
            except (ZeroDivisionError, TypeError):
                raise forms.ValidationError("La taille ne peut pas être zéro et les valeurs doivent être valides.")

        return cleaned_data
    # class OperateurFrom(ModelForm):
#     class Meta:
#         model = User
#         fields = ['nom','prenom','email','date_de_naissance','telephone','anciennete','poste', 'is_operateur'] 

