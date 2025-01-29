from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class RendezVous(models.Model):
    nom = models.CharField(max_length=150, null=True)
    prenom = models.CharField(max_length=150, null=True)
    motif = models.CharField(max_length=100, null=True)
    operateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_operateur': True})
    date_heure = models.DateTimeField(null=True)
    type = models.CharField(null=True, max_length=100, choices=[
        ('physique', 'Physique'),
        ('telephone', 'Téléphone'),
        ('visio', 'Visio')
    ])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['operateur', 'date_heure'], name='unique_rdv_operateur')]
  

class User(AbstractUser):
    date_de_naissance = models.DateField(null = True)
    age = models.IntegerField(null=True)
    telephone = models.CharField( max_length=10,null = True)
    nombre_enfant = models.IntegerField(null=True)
    poids = models.IntegerField(null = True)
    taille = models.IntegerField(null = True)
    imc = models.FloatField(null = True) 
    sexe = models.CharField(max_length=50, null = True)
    region = models.CharField(max_length=100, null = True)
    statut_fumeur = models.CharField(max_length=10, null = True)
    date_souscription = models.DateTimeField(auto_now=False,null = True)
    anciennete = models.IntegerField(default=0, null = True)
    poste = models.CharField(max_length=100, null = True)
    charges = models.FloatField(null=True)
    is_operateur = models.BooleanField(null = True)
    is_client = models.BooleanField(null = True)
    is_prospect = models.BooleanField(null = True)


class Prediction(models.Model):
    nom = models.CharField(max_length=150, null=True)
    prenom = models.CharField(max_length=150, null=True)
    email = models.EmailField(null=True)
    telephone = models.CharField( max_length=10,null = True)
    montant_charges = models.FloatField(default=0)
    date_devis = models.DateField(auto_now=False, auto_now_add=True)
    
