from django.urls import path, include
from .views import AccueilView, AuthentificationView, CouvertureView, DevisView, InscriptionView, ListeOperateurs, EnregistrerOperateur, ListeClients, EnregistrerClient, ListeProspects, EnregistrerProspect, RendezVousView, password_reset, ClientProfil, deconnexion, ModifierProfilView, ModifierOperateur, ModifierCLient, ListeRendezVous, ListePredictions, ModifierPasswordView




urlpatterns = [
    path("", AccueilView.as_view(), name="home"),
    path('liste_prospects_tableau/', ListeProspects.as_view(), name='liste_prospects'),
    path('liste_clients_tableau/', ListeClients.as_view(), name='liste_clients'),
    path('liste_operateurs_tableau/', ListeOperateurs.as_view(), name='liste_operateurs'),
    path('liste_rendez_vous_tableau/', ListeRendezVous.as_view(), name='liste_rendez_vous'),
    path('liste_predictions_tableau/', ListePredictions.as_view(), name='liste_predictions'),
    path('nouveloperateur/', EnregistrerOperateur.as_view(), name = 'enregistrer_operateur'),
    path('nouveauclient/', EnregistrerClient.as_view(), name = 'enregistrer_client'),
    path('nouveauprospect/', EnregistrerProspect.as_view(), name = 'enregistrer_prospect'),

    path("accueil/", AccueilView.as_view(), name="accueil"),
    path("authentification/", AuthentificationView.as_view(), name="authentification"),
    path("couverture/", CouvertureView.as_view(), name="couverture"),
    path("devis/", DevisView.as_view(), name="devis"),
    path("inscription/", InscriptionView.as_view(), name="inscription"),
    path("rendezvous/", RendezVousView.as_view(), name="rendezvous"),
    path("password_reset/", password_reset.as_view(), name="password_reset"),
    path("page_utilisateur_client/", ClientProfil.as_view(), name="page_utilisateur_client"),
    path("deconnexion/", deconnexion, name="deconnexion"),
    path("modifier_profil/", ModifierProfilView.as_view(), name="modifier_profil"),
    path('modifier-password/', ModifierPasswordView.as_view(), name='modifier_password'),
    
    path('liste_operateur/<str:username>/', ModifierOperateur.as_view(), name='detail_operateur'),
    path('liste_clients/<str:username>/', ModifierCLient.as_view(), name='detail_client'),
    path('liste_prospects/<str:username>/', ModifierCLient.as_view(), name='detail_prospect'),

]
