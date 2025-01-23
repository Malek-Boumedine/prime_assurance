from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser

# Create your models here.


class RendezVous(models.Model) : 
    Date_heure = models.DateTimeField()
    # id_client = models.ForeignKey("User", on_delete=models.CASCADE)
    # id_operateur = models.ForeignKey("User", on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    motif = models.CharField(max_length=100)


class User(AbstractUser):

    date_de_naissance = models.DateField(null = True)
    telephone = models.CharField( max_length=10,null = True)
    poids = models.IntegerField(null = True)
    taille = models.IntegerField(null = True)
    imc = models.IntegerField(null = True) #Formule IMC
    sexe = models.BooleanField(null = True)
    statut_fumeur = models.BooleanField(null = True)
    region = models.CharField(max_length=50, null = True)
    date_souscription = models.DateTimeField(auto_now=False,null = True)
    anciennete = models.IntegerField(default=0,null = True)
    is_operateur = models.BooleanField(null = True)
    is_client = models.BooleanField(null = True)
    is_prospect = models.BooleanField(null = True)
    

class Prediction(models.Model):
    id_prospect = models.ForeignKey(User, on_delete=models.CASCADE) # ne pas oublier d'enlever les quotes
    montant_charges = models.FloatField(default=0)
    date_devis = models.DateField(auto_now=False, auto_now_add=True)
