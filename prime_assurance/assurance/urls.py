from django.urls import path, include
from .views import AccueilView, AuthentificationView, CouvertureView, DevisView, InscriptionView, ListeOperateurs, EnregistrerOperateur, ListeClients, EnregistrerClient, ListeProspects, EnregistrerProspect, RendezVousView, ClientProfil, deconnexion, ModifierProfilView, ModifierOperateur, ModifierCLient, ListeRendezVous, ListePredictions, ModifierPasswordView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy




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
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='assurance/password_reset.html',
    email_template_name='assurance/password_reset_email.html',
    subject_template_name='assurance/password_reset_subject.txt',
    success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='assurance/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='assurance/password_reset_confirm.html',
    success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='assurance/password_reset_complete.html'
    ), name='password_reset_complete'),
    
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
    - Gestion des utilisateurs :
        * ListeProspects : Vue pour afficher la liste des prospects.
        * ListeClients : Vue pour afficher la liste des clients.
        * ListeOperateurs : Vue pour afficher la liste des opérateurs.
        * EnregistrerOperateur : Vue pour l'enregistrement d'un opérateur.
        * EnregistrerClient : Vue pour l'enregistrement d'un client.
        * EnregistrerProspect : Vue pour l'enregistrement d'un prospect.

    - Navigation générale :
        * AccueilView : Vue pour la page d'accueil.
        * AuthentificationView : Vue pour la page d'authentification.
        * CouvertureView : Vue pour la page de couverture d'assurance.
        * DevisView : Vue pour la page de devis.
        * InscriptionView : Vue pour la page d'inscription.
        * RendezVousView : Vue pour la page de prise de rendez-vous.

    - Gestion des rendez-vous et des prédictions :
        * ListeRendezVous : Vue pour afficher la liste des rendez-vous.
        * ListePredictions : Vue pour afficher la liste des prédictions.

    - Gestion des mots de passe :
        * password_reset : Vue pour initier la réinitialisation du mot de passe.
        * password_reset_done : Vue affichant la confirmation d'envoi de l'e-mail de réinitialisation.
        * password_reset_confirm : Vue pour confirmer et définir un nouveau mot de passe.
        * password_reset_complete : Vue indiquant la réussite du changement de mot de passe.

    - Gestion du profil et de la connexion :
        * ClientProfil : Vue pour afficher le profil client.
        * ModifierProfilView : Vue pour modifier le profil de l'utilisateur.
        * ModifierPasswordView : Vue pour modifier le mot de passe de l'utilisateur.
        * deconnexion : Vue pour gérer la déconnexion de l'utilisateur.

    - Gestion des modifications :
        * ModifierOperateur : Vue pour modifier un opérateur spécifique.
        * ModifierCLient : Vue pour modifier un client spécifique.
        * ModifierCLient (détail prospect) : Vue pour modifier un prospect spécifique.
"""
