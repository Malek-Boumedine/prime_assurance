from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



# Create your models here.

class RendezVous(models.Model) : 
    Date_heure = models.DateTimeField()
    # id_client = models.ForeignKey("Client", on_delete=models.CASCADE)
    # id_operateur = models.ForeignKey("Client", on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    motif = models.CharField(max_length=100)


class Utilisateur(models.Model) : 
    # id_utilisateur = models.ForeignKey(["Client", "Prospect", "Operateur"], on_delete=models.CASCADE)
    nom_utilisateur = models.CharField(max_length=250)
    mot_de_passe = models.CharField(max_length=250, validators=[MinLengthValidator(12)])
    email = models.CharField(max_length=250)
    prenom = models.CharField(max_length=250)
    nom = models.CharField(max_length=250)
    type_utilisateur = models.CharField(max_length=50)
    
    def creer_utilisateur(self) : 
        User.objects.create_user(
            username=self.nom_utilisateur,
            password=self.mot_de_passe,
            email=self.email,
            first_name=self.prenom, 
            last_name=self.nom
            )


    def authentification(self) :
        nom_saisi = None
        pass_saisi = None
        utilisateur = authenticate(
            username=nom_saisi, 
            password=pass_saisi)
        if utilisateur is not None : 
            print("authentification réussie")
        else : 
            print("echec d'authentification")
            

            
        







