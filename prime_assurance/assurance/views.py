from django.shortcuts import render
from .models import Prediction, User#, Client, Prospect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import OperateurForm
from django.urls import reverse_lazy

# Create your views here.

class Listeoperateurs(ListView):
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
    
# class Listeclients(ListView):
#     model = User
#     template_name = 'assurance/liste_clients.html'
#     context_object_name = 'clients'

#     def get_queryset(self):
#         return User.objects.filter(is_client = 1)
    
# class Listeprospects(ListView):
#     model = User
#     template_name = 'assurance/liste_prospects.html'
#     context_object_name = 'prospects'

#     def get_queryset(self):
#         return User.objects.filter(is_prospect = 1)

