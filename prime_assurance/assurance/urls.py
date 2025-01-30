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
"""
Liste des URL patterns de l'application.

Ces URL patterns sont utilisés pour relier chaque URL aux vues correspondantes de l'application, permettant ainsi 
la navigation vers des pages spécifiques telles que l'accueil, la gestion des utilisateurs (prospects, clients, opérateurs), 
les prédictions, les rendez-vous, ainsi que la gestion du profil utilisateur et des mots de passe.

Attributs :
    AccueilView : Vue pour la page d'accueil.
    ListeProspects : Vue pour afficher la liste des prospects.
    ListeClients : Vue pour afficher la liste des clients.
    ListeOperateurs : Vue pour afficher la liste des opérateurs.
    ListeRendezVous : Vue pour afficher la liste des rendez-vous.
    ListePredictions : Vue pour afficher la liste des prédictions.
    EnregistrerOperateur : Vue pour l'enregistrement d'un opérateur.
    EnregistrerClient : Vue pour l'enregistrement d'un client.
    EnregistrerProspect : Vue pour l'enregistrement d'un prospect.
    AccueilView : Vue pour la page d'accueil.
    AuthentificationView : Vue pour la page d'authentification.
    CouvertureView : Vue pour la page de couverture d'assurance.
    DevisView : Vue pour la page de devis.
    InscriptionView : Vue pour la page d'inscription.
    RendezVousView : Vue pour la page de prise de rendez-vous.
    password_reset : Vue pour réinitialiser le mot de passe.
    ClientProfil : Vue pour afficher le profil client.
    deconnexion : Vue pour gérer la déconnexion de l'utilisateur.
    ModifierProfilView : Vue pour modifier le profil de l'utilisateur.
    ModifierPasswordView : Vue pour modifier le mot de passe de l'utilisateur.
    ModifierOperateur : Vue pour modifier un opérateur spécifique.
    ModifierCLient : Vue pour modifier un client ou un prospect spécifique.
"""
