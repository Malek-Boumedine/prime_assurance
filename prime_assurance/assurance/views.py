from django.shortcuts import redirect, render
from django.views.generic import View, ListView, TemplateView
from .models import Prediction, User
from django.views.generic.edit import CreateView
from .forms import OperateurForm, ClientForm, ProspectForm, DevisForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from .models import User
from . import forms
from .forms import LoginForm
from django.http import HttpResponse


# Create your views here.
#region Operateurs

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

    
class InscriptionView(View):
    template_name = 'assurance/inscription.html'
    success_url = reverse_lazy('accueil')

    def get(self, request):
        form = ClientForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class CouvertureView(View) : 
    template_name = "assurance/couverture.html"
    
    def get(self, request) :
        return render(request, self.template_name)



class DevisView(View) : 
    template_name = "assurance/devis.html"
    success_url = reverse_lazy("accueil")
    
    def get(self, request) :
        form = DevisForm
        return render(request, self.template_name, {"form" : form})
    
    def post(self, request):
        form = DevisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})




class AProposView(View) : 
    template_name = "assurance/apropos.html"
    
    def get(self, request) :
        return render(request, self.template_name)








class ListeOperateurs(ListView):
    model = User
    template_name = "assurance/liste_operateur.html"
    context_object_name = "operateurs"

    def get_queryset(self):
        return User.objects.filter(is_operateur = 1)
    
class EnregistrerOperateur(CreateView):
    model = User
    form_class = OperateurForm
    template_name = 'assurance/enregistrer_operateur.html'
    success_url = reverse_lazy('liste_operateur')

#region clients
    
class ListeClients(ListView):
    model = User
    template_name = 'assurance/liste_clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return User.objects.filter(is_client = 1)

class EnregistrerClient(CreateView):
    model = User
    form_class = ClientForm
    template_name = 'assurance/enregistrer_client.html'
    success_url = reverse_lazy('liste_clients')
    

# region Prospect

class EnregistrerProspect(CreateView):
    model = User
    form_class = ProspectForm
    template_name = 'assurance/enregistrer_prospect.html'
    success_url = reverse_lazy('liste_prospects')


class ListeProspects(ListView):
    model = User
    template_name = 'assurance/liste_prospects.html'
    context_object_name = 'prospects'

    def get_queryset(self):
        return User.objects.filter(is_prospect = 1)
    
