from django.shortcuts import render
from .models import Prediction, User
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import OperateurForm, ClientForm, ProspectForm
from django.urls import reverse_lazy

# Create your views here.
#region Operateurs

class ListeOperateurs(ListView):
    model = User
    template_name = 'assurance/liste_operateur.html'
    context_object_name = 'operateurs'

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
    