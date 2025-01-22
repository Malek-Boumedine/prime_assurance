from django.shortcuts import render
from django.views.generic import ListView
from .models import Utilisateur
from models import Prediction
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import OperateurFrom
from django.urls import reverse_lazy


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

# class Listeoperateur(ListView):
#     model = Operateur
#     template_name = 'assurance/liste_operateur.html'
#     context_object_name = 'operateur'

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         if query:
#             return Operateur.objects.filter(Titre__icontains = query)
#         return Operateur.objects.all()
