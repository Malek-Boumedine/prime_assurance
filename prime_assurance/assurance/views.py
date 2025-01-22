from django.shortcuts import render
from models import Prediction, Operateur#, Client, Prospect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import OperateurFrom
from django.urls import reverse_lazy

# Create your views here.

class Listeoperateur(ListView):
    model = Operateur
    template_name = 'assurance/liste_operateur.html'
    context_object_name = 'operateur'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Operateur.objects.filter(Titre__icontains = query)
        return Operateur.objects.all()
    

