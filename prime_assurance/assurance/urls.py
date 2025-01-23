from django.urls import path, include
from .views import AccueilView, AuthentificationView, CouvertureView, DevisView, AProposView, InscriptionView



urlpatterns = [
    # path("", AccueilView.as_view(), name="accueil"),
    path("accueil/", AccueilView.as_view(), name="accueil"),
    path("authentification/", AuthentificationView.as_view(), name="authentification"),
    path("couverture/", CouvertureView.as_view(), name="couverture"),
    path("devis/", DevisView.as_view(), name="devis"),
    path("apropos/", AProposView.as_view(), name="apropos"),
    path("inscription/", InscriptionView.as_view(), name="inscription"),
    
]


