from django.urls import path
from django.views.generic import TemplateView
from .views import ListeOperateurs, EnregistrerOperateur, ListeClients, EnregistrerClient, ListeProspects, EnregistrerProspect
urlpatterns = [
    path('liste_operateur/', ListeOperateurs.as_view(), name='liste_operateurs'),
    path('liste_clients/', ListeClients.as_view(), name='liste_clients'),
    path('liste_prospects/', ListeProspects.as_view(), name='liste_prospects'),

    path('nouveloperateur/', EnregistrerOperateur.as_view(), name = 'enregistrer_operateur'),
    path('nouveauclient/', EnregistrerClient.as_view(), name = 'enregistrer_client'),
    path('nouveauprospect/', EnregistrerProspect.as_view(), name = 'enregistrer_prospect'),



]
