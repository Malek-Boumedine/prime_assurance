from django.shortcuts import render
from django.views.generic import ListView
from .models import Utilisateur


# Create your views here.

class AuthentificationView(ListView) :
    model = Utilisateur
    template_name = "authentification.html"
    context_object_name = "utilisateurs"
    
    def connexion(self) : 
        utilisateurs = Utilisateur.objects.all().nom_utilisateur
        nom_utilisateur = self.request.GET.get("nom_utilisateur")
        mot_de_passe = self.request.GET.get("mot_de_passe")
        
        if nom_utilisateur in utilisateurs :
            if mot_de_passe == utilisateurs.mot_de_passe : 
                print("connexion OK")
            else : 
                print("mot de passe incorrecte")
        else : 
            print("nom d'utilisateur incorrecte")
    



