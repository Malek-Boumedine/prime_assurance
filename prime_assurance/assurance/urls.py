from django.urls import path, include
from .views import AuthentificationView


urlpatterns = [
    path('authentification', AuthentificationView.as_view(), name="authentification"),
]
