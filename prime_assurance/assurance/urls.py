from django.urls import path
from django.views.generic import TemplateView
from .views import Listeoperateurs, EnregistrerOperateur

urlpatterns = [
    path('liste_operateur/', Listeoperateurs.as_view(), name='liste_operateur'),
    path('nouveloperateur/', EnregistrerOperateur.as_view(), name = 'enregistrer_operateur'),

]
