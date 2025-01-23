from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser

# Create your models here.


class RendezVous(models.Model):
    Date_heure = models.DateTimeField()
    id_client = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, related_name='rdv_client')
    id_operateur = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, related_name='rdv_operateur')
    type = models.CharField(max_length=100)
    motif = models.CharField(max_length=100)

class User(AbstractUser):

    date_de_naissance = models.DateField(null = True)
    age = models.IntegerField(null=True)
    telephone = models.CharField( max_length=10,null = True)
    nombre_enfant = models.IntegerField(null=True)
    poids = models.IntegerField(null = True)
    taille = models.IntegerField(null = True)
    imc = models.IntegerField(null = True) #Formule IMC
    sexe = models.CharField(max_length=10,null = True)
    nombre_enfants = models.IntegerField(null = True)
    statut_fumeur = models.CharField(max_length=3,null = True)
    region = models.CharField(max_length=50, null = True)
    charges = models.IntegerField(null=True)
    date_souscription = models.DateTimeField(auto_now=False,null = True)
    anciennete = models.IntegerField(default=0,null = True)
    poste = models.CharField(max_length=10, choices=[('courtier', 'Courtier'), ('manager', 'Manager')], blank=True, null=True)
    charges = models.FloatField(null=True)
    is_operateur = models.BooleanField(null = True)
    is_client = models.BooleanField(null = True)
    is_prospect = models.BooleanField(null = True)


class Prediction(models.Model):
    id_prospect = models.ForeignKey(User, on_delete=models.CASCADE) # ne pas oublier d'enlever les quotes
    montant_charges = models.FloatField(default=0)
    date_devis = models.DateField(auto_now=False, auto_now_add=True)
