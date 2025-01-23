from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from .models import User
from . import forms
from .forms import LoginForm
from django.http import HttpResponse


# Create your views here.

class AccueilView(View) : 
    template_name = "assurance/accueil.html"
    
    def get(self, request) :
        return render(request, self.template_name)


class AuthentificationView(View):
    template_name = "assurance/authentification.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                message = f"Bienvenue {user.username}! Vous êtes maintenant connecté. Vous allez être redirigé vers votre espace personnel"
            else:
                message = "Identifiants invalides."
        return render(request, self.template_name, {"form": form, "message": message})
    
    
class CouvertureView(View) : 
    template_name = "assurance/couverture.html"
    
    def get(self, request) :
        return render(request, self.template_name)


class DevisView(View) : 
    template_name = "assurance/devis.html"
    
    def get(self, request) :
        return render(request, self.template_name)


class AProposView(View) : 
    template_name = "assurance/apropos.html"
    
    def get(self, request) :
        return render(request, self.template_name)


class InscriptionView(View) : 
    template_name = "assurance/inscription.html"
    
    def get(self, request) :
        return render(request, self.template_name)




class Listeoperateur(ListView):
    model = User
    template_name = "assurance/liste_operateur.html"
    context_object_name = "operateurs"

    def get_queryset(self):
        return User.objects.filter(is_operateur = 1)
