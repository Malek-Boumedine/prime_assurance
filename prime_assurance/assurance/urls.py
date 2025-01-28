from django.urls import path, include
from .views import AccueilView, AuthentificationView, CouvertureView, DevisView, InscriptionView, ListeOperateurs, EnregistrerOperateur, ListeClients, EnregistrerClient, ListeProspects, EnregistrerProspect, RendezVous, password_reset, ClientProfil, deconnexion, ModifierProfilView
from django.views.generic import TemplateView




urlpatterns = [
    path("", AccueilView.as_view(), name="home"),  # Ajout pour gérer l'URL racine

    path('liste_operateur/', ListeOperateurs.as_view(), name='liste_operateurs'),
    path('liste_clients/', ListeClients.as_view(), name='liste_clients'),
    path('liste_prospects/', ListeProspects.as_view(), name='liste_prospects'),

    path('nouveloperateur/', EnregistrerOperateur.as_view(), name = 'enregistrer_operateur'),
    path('nouveauclient/', EnregistrerClient.as_view(), name = 'enregistrer_client'),
    path('nouveauprospect/', EnregistrerProspect.as_view(), name = 'enregistrer_prospect'),

    path("accueil/", AccueilView.as_view(), name="accueil"),
    path("authentification/", AuthentificationView.as_view(), name="authentification"),
    path("couverture/", CouvertureView.as_view(), name="couverture"),
    path("devis/", DevisView.as_view(), name="devis"),
    path("inscription/", InscriptionView.as_view(), name="inscription"),
    path("rendezvous/", RendezVous.as_view(), name="rendezvous"),
    path("password_reset/", password_reset.as_view(), name="password_reset"),
    path("page_utilisateur_client/", ClientProfil.as_view(), name="page_utilisateur_client"),
    path("deconnexion/", deconnexion, name="deconnexion"),
    path("modifier_profil/", ModifierProfilView.as_view(), name="modifier_profil"),
    
]
