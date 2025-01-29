from django.shortcuts import redirect, render
from django.views.generic import View, ListView, TemplateView, DetailView, UpdateView
from .models import Prediction, User
from django.views.generic.edit import CreateView, UpdateView
from .forms import OperateurForm, ClientForm, ProspectForm, DevisForm, ModifierProfilForm, RendezVousForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import User
from . import forms
from .forms import LoginForm
from django.http import HttpResponse
import datetime




# Create your views here.

class AccueilView(View) : 
    template_name = "assurance/accueil.html"
    
    def get(self, request) :
        return render(request, self.template_name)


class AuthentificationView(View):
    template_name = "assurance/authentification.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("page_utilisateur_client")
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
                return redirect("page_utilisateur_client")
                
            else:
                message = "Identifiants invalides."
        return render(request, self.template_name, {"form": form, "message": message})


def deconnexion(request):
    logout(request)
    return redirect('accueil')

    
class InscriptionView(View):
    template_name = 'assurance/inscription.html'
    success_url = reverse_lazy('accueil')

    def get(self, request):
        form = ProspectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProspectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class password_reset(View) : 
    template_name = "assurance/password_reset.html"
    
    def get(self, request) :
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get("email")
        return redirect("url de reset")


class CouvertureView(View) : 
    template_name = "assurance/couverture.html"
    
    def get(self, request) :
        return render(request, self.template_name)


class DevisView(View):
    template_name = "assurance/devis.html"

    def get(self, request):
        form = DevisForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = DevisForm(request.POST)
        if form.is_valid():
            montant = form.calculer()
            # Créer et sauvegarder la prédiction
            prediction = Prediction(nom=form.cleaned_data['last_name'], prenom=form.cleaned_data['first_name'], email=form.cleaned_data['email'], telephone=form.cleaned_data['telephone'], montant_charges=montant)
            prediction.save()
            messages.success(request, f"Le montant estimé de votre assurance est de {montant:.2f} €")
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class ModifierProfilView(View):
    template_name = 'assurance/modifier_profil.html'

    def get(self, request):
        form = ModifierProfilForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ModifierProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès!")
            return redirect('page_utilisateur_client') 


class RendezVous(View):
    template_name = "assurance/rendezvous.html"

    def get(self, request):
        form = RendezVousForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save(commit=False)
            rdv.id_client = request.user
            rdv.save()
            messages.success(request, "Rendez-vous enregistré avec succès !")
            return redirect('page_utilisateur_client')
        return render(request, self.template_name, {'form': form})


class ListeOperateurs(ListView):
    model = User
    template_name = "assurance/liste_operateurs_tableau.html"
    context_object_name = "operateurs"

    def get_queryset(self):
        return User.objects.filter(is_operateur = 1)
    
    def post(self, request):
        username = request.POST.get('username')

        if username:
            opetateur = User.objects.filter(username = username).first()
            
            if opetateur:
                opetateur.delete()

                return redirect('/liste_operateurs_tableau')
    
    
class EnregistrerOperateur(CreateView):
    model = User
    form_class = OperateurForm
    template_name = 'assurance/enregistrer_operateur.html'
    success_url = reverse_lazy('liste_operateurs')


class ModifierOperateur(View):
    def get(self, request, username):
        # Récupérer l'opérateur à partir de l'username
        operateur = User.objects.get(username=username)
        form = OperateurForm(instance=operateur)
        return render(request, 'assurance/detail_operateur.html', {'form': form, 'operateur': operateur})

    def post(self, request, username):
        # Récupérer l'opérateur à partir de l'username
        operateur = User.objects.get(username=username)
        form = OperateurForm(request.POST, instance=operateur)

        if form.is_valid():
            form.save()  # Sauvegarder les données modifiées
            return redirect('/liste_operateurs_tableau/')  # Rediriger vers la liste des opérateurs

        return render(request, 'assurance/detail_operateur.html', {'form': form, 'operateur': operateur})
    

class ListeClients(ListView):
    model = User
    template_name = 'assurance/liste_clients_tableau.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return User.objects.filter(is_client = 1)
    
    def post(self, request):
        username = request.POST.get('username')

        if username:
            client = User.objects.filter(username = username).first()
            
            if client:
                client.delete()

                return redirect('/liste_clients_tableau')


class EnregistrerClient(CreateView):
    model = User
    form_class = ClientForm
    template_name = 'assurance/enregistrer_client.html'
    success_url = reverse_lazy('liste_clients')
    

class ModifierCLient(View):
    def get(self, request, username):
        client = User.objects.get(username=username)
        form = ClientForm(instance=client)
        return render(request, 'assurance/detail_client.html', {'form': form, 'client': client})

    def post(self, request, username):
        client = User.objects.get(username=username)
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()  
            return redirect('/liste_clients_tableau/')  

        return render(request, 'assurance/detail_client.html', {'form': form, 'client': client})


class EnregistrerProspect(CreateView):
    model = User
    form_class = ProspectForm
    template_name = 'assurance/enregistrer_prospect.html'
    success_url = reverse_lazy('liste_prospects')


class ListeProspects(ListView):
    model = User
    template_name = 'assurance/liste_prospects_tableau.html'
    context_object_name = 'prospects'

    def get_queryset(self):
        return User.objects.filter(is_prospect = 1)
    
    def post(self, request):
       
        username_delete = request.POST.get('username_delete')
        print(request.POST)

        if username_delete:
            prospect = User.objects.filter(username = username_delete).first()
            
            if prospect:
                prospect.delete()

                

        username_client = request.POST.get('username_client')

        if username_client:
            prospect = User.objects.filter(username = username_client).first()
            
            if prospect:
                prospect.is_prospect = False
                prospect.is_client = True
                prospect.save()
            


        return redirect('/liste_prospects_tableau')
    
class ModifierProspect(View):
    def get(self, request, username):
        prospect = User.objects.get(username=username)
        form = ProspectForm(instance=prospect)
        return render(request, 'assurance/detail_prospect.html', {'form': form, 'prospect': prospect})

    def post(self, request, username):
        prospect = User.objects.get(username=username)
        form = ProspectForm(request.POST, instance=prospect)

        if form.is_valid():
            form.save()  
            return redirect('/liste_prospects_tableau/')  

        return render(request, 'assurance/detail_prospect.html', {'form': form, 'prospect': prospect})


class ClientProfil(ListView):
    model = User 
    template_name = 'assurance/page_utilisateur_client.html'
    context_object_name = 'client'  
    
    def get_queryset(self):
        username = self.request.user.username
        return User.objects.filter(username = username)[0]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.is_client = True
        user.is_prospect = False
        user.date_souscription = datetime.datetime.now()
        user.save()
        messages.success(request, "Vous êtes maintenant client!")
        return redirect('page_utilisateur_client')   
    
      
    
    