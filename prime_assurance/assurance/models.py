from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    date_de_naissance = models.DateField()
    telephone = models.CharField( max_length=10)
    poids = models.IntegerField()
    taille = models.IntegerField()
    imc = models.IntegerField() #Formule IMC
    sexe = models.BooleanField()
    statut_fumeur = models.BooleanField()
    region = models.CharField(max_length=50)
    date_souscription = models.DateTimeField(auto_now=False)
    anciennete = models.IntegerField(default=0)
    is_operateur = models.BooleanField()
    is_client = models.BooleanField()
    is_propect = models.BooleanField()
    

    


class Prediction(models.Model):
    id_prospect = models.ForeignKey(User, on_delete=models.CASCADE) # ne pas oublier d'enlever les quotes
    montant_charges = models.FloatField(default=0)
    date_devis = models.DateField(auto_now=False, auto_now_add=True)