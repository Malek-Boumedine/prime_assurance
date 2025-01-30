from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime



# Create your models here.

class User(AbstractUser):
    first_name = models.CharField("Prénom", max_length=150, blank=True)
    last_name = models.CharField("Nom", max_length=150, blank=True)
    date_de_naissance = models.DateField(null = True, default='1970-01-01')
    age = models.IntegerField(null=True, default=0)
    telephone = models.CharField( max_length=10,null = True, default=0000000000)
    nombre_enfant = models.IntegerField(null=True, default=0)
    poids = models.IntegerField(null = True, default=0)
    taille = models.IntegerField(null = True, default=0)
    imc = models.FloatField(null = True, default=0)
    sexe = models.CharField(max_length=50, null = True, default=0)
    region = models.CharField(max_length=100, null = True, default=0)
    statut_fumeur = models.CharField(max_length=10, null = True, default=0)
    date_souscription = models.DateTimeField(auto_now=False,null = True)
    anciennete = models.IntegerField(default=0, null = True)
    poste = models.CharField(max_length=100, null = True, default="Courtier")
    charges = models.FloatField(null=True, default=0)
    is_operateur = models.BooleanField(null = True, default=0)
    is_client = models.BooleanField(null = True, default=0)
    is_prospect = models.BooleanField(null = True, default=0)


class RendezVous(models.Model):
    prenom = models.CharField(max_length=150, null=True)
    nom = models.CharField(max_length=150, null=True)
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


class Prediction(models.Model):
    nom = models.CharField(max_length=150, null=True)
    prenom = models.CharField(max_length=150, null=True)
    email = models.EmailField(null=True)
    telephone = models.CharField( max_length=10,null = True)
    montant_charges = models.FloatField(default=0)
    date_devis = models.DateField(auto_now=False, auto_now_add=True)
    
