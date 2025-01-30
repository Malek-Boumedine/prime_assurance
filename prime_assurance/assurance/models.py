from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime



# Create your models here.

class User(AbstractUser):
    """
    Modèle représentant un utilisateur de l'application.

    Ce modèle étend le modèle de base `AbstractUser` de Django et inclut des informations supplémentaires 
    concernant l'utilisateur, telles que ses coordonnées personnelles, son IMC, son statut fumeur, ses charges 
    d'assurance, ainsi que son statut d'opérateur, de client ou de prospect.

    Attributs :
        first_name (CharField) : Prénom de l'utilisateur.
        last_name (CharField) : Nom de l'utilisateur.
        date_de_naissance (DateField) : Date de naissance de l'utilisateur.
        age (IntegerField) : Âge de l'utilisateur, calculé à partir de la date de naissance.
        telephone (CharField) : Numéro de téléphone de l'utilisateur.
        nombre_enfant (IntegerField) : Nombre d'enfants de l'utilisateur.
        poids (IntegerField) : Poids de l'utilisateur en kilogrammes.
        taille (IntegerField) : Taille de l'utilisateur en centimètres.
        imc (FloatField) : Indice de masse corporelle de l'utilisateur.
        sexe (CharField) : Sexe de l'utilisateur.
        region (CharField) : Région géographique de l'utilisateur.
        statut_fumeur (CharField) : Statut fumeur de l'utilisateur (Oui ou Non).
        date_souscription (DateTimeField) : Date de souscription de l'utilisateur.
        anciennete (IntegerField) : Ancienneté de l'utilisateur dans l'entreprise.
        poste (CharField) : Poste occupé par l'utilisateur (par défaut, "Courtier").
        charges (FloatField) : Charges d'assurance estimées pour l'utilisateur.
        is_operateur (BooleanField) : Indicateur si l'utilisateur est un opérateur.
        is_client (BooleanField) : Indicateur si l'utilisateur est un client.
        is_prospect (BooleanField) : Indicateur si l'utilisateur est un prospect.
    """
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
    """
    Modèle représentant un rendez-vous avec un opérateur.

    Ce modèle permet de gérer les rendez-vous des clients avec des opérateurs. Il inclut des informations 
    telles que le prénom et le nom du client, le motif du rendez-vous, l'opérateur assigné, l'heure et la date du rendez-vous,
    ainsi que le type de rendez-vous (physique, téléphone ou visio).

    Attributs :
        prenom (CharField) : Prénom du client.
        nom (CharField) : Nom du client.
        motif (CharField) : Motif du rendez-vous.
        operateur (ForeignKey) : L'opérateur assigné au rendez-vous, lié à un utilisateur de type opérateur.
        date_heure (DateTimeField) : Date et heure du rendez-vous.
        type (CharField) : Type de rendez-vous (physique, téléphone, visio).
    
    Contraintes :
        unique_rdv_operateur : Assure qu'il n'y a pas de doublon de rendez-vous pour un même opérateur à la même date et heure.
    """
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
    """
    Modèle représentant une prédiction de charges d'assurance.

    Ce modèle permet de stocker les informations relatives à une prédiction de charges d'assurance pour un utilisateur. 
    Il inclut des informations personnelles telles que le nom, le prénom, l'email, le téléphone, ainsi que le montant 
    des charges estimées et la date du devis.

    Attributs :
        nom (CharField) : Nom de l'utilisateur.
        prenom (CharField) : Prénom de l'utilisateur.
        email (EmailField) : Email de l'utilisateur.
        telephone (CharField) : Numéro de téléphone de l'utilisateur.
        montant_charges (FloatField) : Montant des charges d'assurance estimées pour l'utilisateur.
        date_devis (DateField) : Date de création du devis.
    """
    nom = models.CharField(max_length=150, null=True)
    prenom = models.CharField(max_length=150, null=True)
    email = models.EmailField(null=True)
    telephone = models.CharField( max_length=10,null = True)
    montant_charges = models.FloatField(default=0)
    date_devis = models.DateField(auto_now=False, auto_now_add=True)
    
