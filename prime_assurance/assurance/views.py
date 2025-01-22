from django.shortcuts import render
from models import Prediction, User#, Client, Prospect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import OperateurFrom
from django.urls import reverse_lazy

# Create your views here.

class Listeoperateur(ListView):
    model = User
    template_name = 'assurance/liste_operateur.html'
    context_object_name = 'operateurs'

    def get_queryset(self):
        return User.objects.filter(is_operateur = 1)
    

