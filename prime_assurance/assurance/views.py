from django.shortcuts import redirect, render
from django.views.generic import View, ListView, FormView
from .models import Prediction, User, RendezVous
from django.views.generic.edit import CreateView
from .forms import OperateurForm, ClientForm, ProspectForm, DevisForm, ModifierProfilForm, RendezVousForm, LoginForm, ContactForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
import datetime




# Create your views here.

# region Accueil

class AccueilView(View):
    """
    Vue pour la page d'accueil.

    Cette vue gère l'affichage de la page d'accueil ainsi que le traitement du formulaire de contact.
    Elle permet aux utilisateurs d'envoyer un message via un formulaire.
    """
    template_name = "assurance/accueil.html"

    def get(self, request):
        """
        Gère les requêtes GET pour afficher la page d'accueil.

        Args:
            request (HttpRequest): La requête HTTP entrante.

        Returns:
            HttpResponse: La réponse contenant le rendu du template d'accueil.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Gère les requêtes POST pour traiter le formulaire de contact.

        Vérifie si tous les champs du formulaire sont remplis et tente d'envoyer un e-mail
        contenant le message soumis. Affiche un message de succès ou d'erreur en fonction du résultat.

        Args:
            request (HttpRequest): La requête HTTP contenant les données du formulaire.

        Returns:
            HttpResponseRedirect: Redirige l'utilisateur vers la page d'accueil après traitement du formulaire.
        """
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if nom and email and message:
            try:
                send_mail(
                    subject=f'Nouveau message de {nom}',
                    message=f'De: {email}\n\nMessage:\n{message}',
                    from_email='alghom.ia@gmail.com',
                    recipient_list=['assur.aimant59@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Votre message a été envoyé avec succès!")
            except Exception as e:
                messages.error(request, "Une erreur s'est produite lors de l'envoi du message.")
        else:
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
        return redirect('accueil')


# region Authentification
class AuthentificationView(View):
    """
    Vue pour gérer l'authentification des utilisateurs.

    Cette vue est responsable de l'affichage du formulaire de connexion, de la gestion de la soumission
    du formulaire pour authentifier un utilisateur, et de la redirection vers la page utilisateur si l'utilisateur
    est déjà connecté.

    Attributs :
        template_name (str) : Le nom du template à utiliser pour afficher la page de connexion.

    Méthodes :
        get(request) : Récupère la requête GET, affiche le formulaire de connexion si l'utilisateur n'est pas connecté, 
                       ou redirige vers la page utilisateur si l'utilisateur est déjà authentifié.
        post(request) : Traite la soumission du formulaire de connexion en validant les identifiants de l'utilisateur.
    """
    template_name = "assurance/authentification.html"
    
    def get(self, request):
        """
        Gère la requête GET pour afficher le formulaire de connexion.

        Si l'utilisateur est déjà authentifié, il est redirigé vers la page de son profil. 
        Sinon, un formulaire de connexion est affiché.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP GET.

        Retour :
            HttpResponseRedirect ou HttpResponse : Si l'utilisateur est authentifié, redirige vers la page utilisateur,
                                                  sinon renvoie la page avec le formulaire de connexion.
        """
        if request.user.is_authenticated:
            return redirect("page_utilisateur_client")
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """
        Gère la soumission du formulaire de connexion.

        Valide les identifiants soumis dans le formulaire. Si les identifiants sont corrects, l'utilisateur est
        authentifié et redirigé vers sa page. Si les identifiants sont invalides, un message d'erreur est affiché.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP POST contenant les données soumises par l'utilisateur.

        Retour :
            HttpResponse : Renvoie la page de connexion avec soit un message d'erreur si les identifiants sont invalides,
                           soit redirige vers la page utilisateur si la connexion est réussie.
        """
        form = LoginForm(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"],)
            if user is not None:
                login(request, user)
                return redirect("page_utilisateur_client")
            else:
                message = "Identifiants invalides."
        return render(request, self.template_name, {"form": form, "message": message})


# region Deconnexion
def deconnexion(request):
    """
    Gère la déconnexion de l'utilisateur.

    Cette fonction déconnecte l'utilisateur actuellement connecté et le redirige vers la page d'accueil.

    Arguments :
        request (HttpRequest) : L'objet de la requête HTTP.

    Retour :
        HttpResponseRedirect : Redirige l'utilisateur vers la page d'accueil après la déconnexion.
    """
    logout(request)
    return redirect('accueil')


# region Inscription
class InscriptionView(View):
    """
    Vue pour l'inscription d'un prospect.

    Cette vue permet à un utilisateur de s'inscrire en remplissant un formulaire. 
    En cas de soumission valide, le prospect est enregistré et l'utilisateur est redirigé vers la page d'accueil.

    Attributs :
        template_name (str) : Le nom du template à utiliser pour rendre la page.
        success_url (str) : L'URL vers laquelle rediriger après une inscription réussie.

    Méthodes :
        get(request) : Gère la requête GET et rend le formulaire d'inscription.
        post(request) : Gère la soumission du formulaire d'inscription, valide les données et enregistre le prospect.
    """
    template_name = 'assurance/inscription.html'
    success_url = reverse_lazy('accueil')

    def get(self, request):
        """
        Gère la requête GET pour afficher le formulaire d'inscription.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP.

        Retour :
            HttpResponse : La page de formulaire d'inscription avec le formulaire vide.
        """
        form = ProspectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Gère la soumission du formulaire d'inscription et enregistre le prospect.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP.

        Retour :
            HttpResponseRedirect : Redirige vers la page d'accueil si l'inscription réussie, sinon réaffiche le formulaire avec des erreurs.
        """
        form = ProspectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


# region Couverture
class CouvertureView(View) : 
    """
    Vue pour afficher la page de couverture d'assurance.

    Cette vue rend la page d'information sur les couvertures d'assurance proposées.

    Attributs :
        template_name (str) : Le nom du template à utiliser pour rendre la page de couverture.

    Méthodes :
        get(request) : Gère la requête GET et rend la page de couverture.
    """
    template_name = "assurance/couverture.html"
    
    def get(self, request) :
        """
        Gère la requête GET pour afficher la page de couverture d'assurance.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP.

        Retour :
            HttpResponse : La page de couverture d'assurance.
        """
        return render(request, self.template_name)


# region Devis
class DevisView(View):
    """
    Vue pour afficher la page de devis d'assurance.

    Cette vue permet à l'utilisateur de calculer une estimation de ses charges d'assurance
    en fonction des informations fournies dans le formulaire. Si les informations sont valides,
    un devis est généré et affiché.

    Attributs :
        template_name (str) : Le nom du template à utiliser pour rendre la page de devis.

    Méthodes :
        get(request) : Gère la requête GET et rend la page de devis avec un formulaire vide.
        post(request) : Gère la requête POST pour traiter les données soumises et calculer le devis.
    """
    template_name = "assurance/devis.html"

    def get(self, request):
        """
        Gère la requête GET pour afficher la page de devis d'assurance avec un formulaire vide.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP.

        Retour :
            HttpResponse : La page de devis contenant le formulaire.
        """
        form = DevisForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        """
        Gère la requête POST pour calculer un devis d'assurance en fonction des informations soumises.

        Si les informations du formulaire sont valides, un montant est calculé et un devis est enregistré.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP contenant les données du formulaire.

        Retour :
            HttpResponse : La page de devis avec le montant calculé ou le formulaire si des erreurs sont présentes.
        """
        form = DevisForm(request.POST)
        if form.is_valid():
            montant = form.calculer()
            prediction = Prediction(nom=form.cleaned_data['last_name'], prenom=form.cleaned_data['first_name'], email=form.cleaned_data['email'], telephone=form.cleaned_data['telephone'], montant_charges=montant)
            prediction.save()
            messages.success(request, f"Le montant estimé de votre assurance est de {montant:.2f} €")
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


# region Modifier profil
class ModifierProfilView(View):
    """
    Vue permettant à un utilisateur de modifier son profil.

    Cette vue affiche un formulaire pré-rempli avec les informations actuelles de l'utilisateur
    et permet de mettre à jour son profil après validation des données soumises.

    Attributs :
        template_name (str) : Le nom du template utilisé pour afficher la page de modification du profil.

    Méthodes :
        get(request) : Affiche le formulaire de modification du profil avec les données de l'utilisateur.
        post(request) : Traite les données soumises par le formulaire et met à jour le profil de l'utilisateur.
    """
    template_name = 'assurance/modifier_profil.html'

    def get(self, request):
        """
        Gère la requête GET pour afficher le formulaire de modification du profil avec les informations actuelles.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP.

        Retour :
            HttpResponse : La page contenant le formulaire pré-rempli avec les informations du profil.
        """
        form = ModifierProfilForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """
        Gère la requête POST pour mettre à jour le profil de l'utilisateur avec les nouvelles informations soumises.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP contenant les données du formulaire.

        Retour :
            HttpResponse : La page de profil utilisateur après la mise à jour ou un message d'erreur en cas d'échec.
        """
        form = ModifierProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès!")
            return redirect('page_utilisateur_client') 


# region Mot de passe
class ModifierPasswordView(LoginRequiredMixin, FormView):
    """
    Vue permettant à un utilisateur de modifier son mot de passe.

    Cette vue affiche un formulaire de changement de mot de passe et valide la nouvelle
    information avant de mettre à jour le mot de passe de l'utilisateur.

    Attributs :
        template_name (str) : Le nom du template utilisé pour afficher la page de modification du mot de passe.
        form_class (Form) : La classe de formulaire utilisée pour saisir le nouveau mot de passe.
        success_url (str) : L'URL vers laquelle l'utilisateur sera redirigé après la modification réussie du mot de passe.

    Méthodes :
        get_form_kwargs() : Prépare les arguments pour initialiser le formulaire de mot de passe.
        form_valid(form) : Traite le formulaire valide, met à jour le mot de passe et réinitialise la session d'authentification.
        form_invalid(form) : Gère les cas où le formulaire est invalide.
    """
    template_name = 'assurance/modifier_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('page_utilisateur_client')

    def get_form_kwargs(self):
        """
        Prépare les arguments pour initialiser le formulaire de mot de passe.

        Arguments :
            Aucun.

        Retour :
            dict : Dictionnaire des arguments pour initialiser le formulaire, incluant l'utilisateur actuel et, si la requête est POST, les données soumises.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == "POST":
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        """
        Traite le formulaire valide, met à jour le mot de passe et réinitialise la session d'authentification.

        Arguments :
            form (Form) : Le formulaire valide contenant les nouvelles informations de mot de passe.

        Retour :
            HttpResponse : Redirection vers l'URL de succès après une mise à jour réussie du mot de passe.
        """
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Votre mot de passe a été modifié avec succès!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Gère les cas où le formulaire est invalide.

        Arguments :
            form (Form) : Le formulaire invalide.

        Retour :
            HttpResponse : Retourne le formulaire invalide à la vue pour afficher les erreurs.
        """
        return super().form_invalid(form)
        
    
####################
# region predictions
####################

class ListePredictions(ListView):
    """
    Vue pour afficher la liste des prédictions d'assurance.

    Cette vue permet d'afficher un tableau listant toutes les prédictions d'assurance existantes dans le système. 
    Elle fournit également une fonctionnalité de suppression d'une prédiction via une requête POST, en supprimant l'élément 
    spécifié par son ID.

    Attributs :
        model (Prediction) : Le modèle associé pour récupérer les prédictions.
        template_name (str) : Le nom du template utilisé pour afficher la liste des prédictions.
        context_object_name (str) : Le nom de la variable dans le contexte contenant la liste des prédictions.

    Méthodes :
        post(request) : Supprime une prédiction spécifique en fonction de l'ID fourni dans la requête POST.
    """
    model = Prediction
    template_name = "assurance/liste_predictions_tableau.html"
    context_object_name = "predictions"

    def post(self, request):
        """
        Supprime une prédiction spécifique basée sur l'ID fourni dans la requête POST.

        Cette méthode traite une requête POST qui contient un `prediction_id`. Si l'ID est trouvé, 
        la prédiction correspondante est supprimée de la base de données, puis l'utilisateur est redirigé vers 
        la liste des prédictions.

        Arguments :
            request (HttpRequest) : L'objet de la requête HTTP contenant les données de la requête POST.

        Retour :
            HttpResponseRedirect : Redirige l'utilisateur vers la page de la liste des prédictions après la suppression.
        """
        prediction_id = request.POST.get('prediction_id')
        if prediction_id:
            prediction = Prediction.objects.get(id=prediction_id)
            prediction.delete()
            return redirect('/liste_predictions_tableau')


####################
# region Rendez-vous
####################

class RendezVousView(View):
    """
    Vue permettant de créer un rendez-vous.

    Cette vue permet à un utilisateur de créer un rendez-vous via un formulaire. 
    Elle gère l'affichage du formulaire (GET) et l'enregistrement des données (POST).

    Attributs :
        template_name (str) : Le template utilisé pour afficher la page.
    """
    template_name = "assurance/rendezvous.html"

    def get(self, request):
        """
        Gère la requête GET pour afficher le formulaire de création de rendez-vous.

        Arguments :
            request : La requête HTTP.

        Retourne :
            HttpResponse : Affiche le formulaire de rendez-vous.
        """
        form = RendezVousForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Gère la soumission du formulaire de création de rendez-vous.

        Cette méthode est appelée lorsque le formulaire est soumis. Si le formulaire est valide,
        elle enregistre le rendez-vous et le lie à l'utilisateur connecté, puis affiche un message 
        de succès et redirige vers la page de profil de l'utilisateur.

        Arguments :
            request : La requête HTTP contenant les données du formulaire.

        Retourne :
            HttpResponse : Si le formulaire est valide, redirige vers la page utilisateur. Sinon, 
            réaffiche le formulaire avec des erreurs.
        """
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save(commit=False)
            rdv.id_client = request.user
            rdv.save()
            messages.success(request, "Rendez-vous enregistré avec succès !")
            return redirect('page_utilisateur_client')
        return render(request, self.template_name, {'form': form})


class ListeRendezVous(ListView):
    """
    Vue permettant d'afficher la liste des rendez-vous et de supprimer un rendez-vous.

    Cette vue gère l'affichage de tous les rendez-vous sous forme de tableau (GET) 
    et la suppression d'un rendez-vous spécifique (POST) via un identifiant.

    Attributs :
        model (class) : Le modèle utilisé pour récupérer les données de la base (RendezVous).
        template_name (str) : Le template utilisé pour afficher la liste des rendez-vous.
        context_object_name (str) : Le nom du contexte dans le template (ici "rendezvous").
    """
    model = RendezVous
    template_name = "assurance/liste_rendez_vous_tableau.html"
    context_object_name = "rendezvous"

    def post(self, request):
        """
        Gère la suppression d'un rendez-vous spécifique.

        Cette méthode est appelée lorsqu'une requête POST est envoyée avec l'identifiant d'un rendez-vous à supprimer.
        Si un `rdv_id` est fourni, le rendez-vous correspondant est supprimé de la base de données.

        Arguments :
            request : La requête HTTP contenant l'identifiant du rendez-vous à supprimer.

        Retourne :
            HttpResponse : Redirige vers la liste des rendez-vous après la suppression.
        """
        rdv_id = request.POST.get('rdv_id')
        if rdv_id:
            rendez_vous = RendezVous.objects.get(id=rdv_id)
            rendez_vous.delete()
            return redirect('/liste_rendez_vous_tableau')


##################
# region opérateur
##################

class ListeOperateurs(ListView):
    """
    Vue permettant d'afficher la liste des opérateurs et de supprimer un opérateur spécifique.

    Cette vue permet d'afficher tous les utilisateurs ayant le statut d'opérateur (GET) 
    et de supprimer un opérateur spécifique via son nom d'utilisateur (POST).

    Attributs :
        model (class) : Le modèle utilisé pour récupérer les données de la base (User).
        template_name (str) : Le template utilisé pour afficher la liste des opérateurs.
        context_object_name (str) : Le nom du contexte dans le template (ici "operateurs").

    Méthodes :
        get_queryset() : Filtre et retourne la liste des utilisateurs ayant le statut d'opérateur.
        post() : Gère la suppression d'un opérateur en fonction du nom d'utilisateur fourni.
    """
    model = User
    template_name = "assurance/liste_operateurs_tableau.html"
    context_object_name = "operateurs"

    def get_queryset(self):
        """
        Filtre et retourne les utilisateurs ayant le statut d'opérateur.

        Cette méthode est utilisée pour récupérer la liste des opérateurs (utilisateurs avec 
        l'attribut `is_operateur` égal à 1) pour l'affichage dans le template.

        Retourne :
            queryset : Liste des utilisateurs ayant le statut d'opérateur.
        """
        return User.objects.filter(is_operateur = 1)
    
    def post(self, request):
        """
        Gère la suppression d'un opérateur spécifique via son nom d'utilisateur.

        Cette méthode est appelée lorsqu'une requête POST est envoyée avec le nom d'utilisateur 
        d'un opérateur à supprimer. Si un opérateur avec ce nom d'utilisateur existe, il est supprimé 
        de la base de données.

        Arguments :
            request : La requête HTTP contenant le nom d'utilisateur de l'opérateur à supprimer.

        Retourne :
            HttpResponse : Redirige vers la liste des opérateurs après la suppression.
        """
        username = request.POST.get('username')
        if username:
            opetateur = User.objects.filter(username = username).first()
            if opetateur:
                opetateur.delete()
                return redirect('/liste_operateurs_tableau')
    

class EnregistrerOperateur(CreateView):
    """
    Vue permettant d'enregistrer un nouvel opérateur.

    Cette vue utilise un formulaire pour créer un nouvel utilisateur avec le statut d'opérateur 
    et le sauvegarder dans la base de données.

    Attributs :
        model (class) : Le modèle utilisé pour créer un nouvel opérateur (User).
        form_class (class) : Le formulaire à utiliser pour la création de l'opérateur (OperateurForm).
        template_name (str) : Le template utilisé pour afficher le formulaire d'enregistrement.
        success_url (str) : L'URL vers laquelle l'utilisateur sera redirigé après un enregistrement réussi.
    """
    model = User
    form_class = OperateurForm
    template_name = 'assurance/enregistrer_operateur.html'
    success_url = reverse_lazy('liste_operateurs')


class ModifierOperateur(View):
    """
    Vue permettant de modifier les informations d'un opérateur existant.

    Cette vue permet de récupérer un opérateur en fonction de son `username`, 
    d'afficher ses informations dans un formulaire pré-rempli et de les modifier 
    lorsqu'un formulaire valide est soumis.

    Attributs :
        get(request, username) : Récupère l'opérateur à partir de son `username` et affiche un formulaire 
                                 avec ses informations actuelles.
        post(request, username) : Récupère l'opérateur, met à jour ses informations si le formulaire est valide, 
                                  puis redirige vers la liste des opérateurs.
    """
    def get(self, request, username):
        """
        Récupère un opérateur par son `username` et affiche un formulaire 
        pré-rempli avec ses informations actuelles.

        Args:
            request (HttpRequest): L'objet de requête.
            username (str): Le nom d'utilisateur de l'opérateur à récupérer.

        Returns:
            HttpResponse: La réponse avec le formulaire pré-rempli pour modification.
        """
        # Récupérer l'opérateur à partir de l'username
        operateur = User.objects.get(username=username)
        form = OperateurForm(instance=operateur)
        return render(request, 'assurance/detail_operateur.html', {'form': form, 'operateur': operateur})

    def post(self, request, username):
        """
        Récupère un opérateur par son `username`, met à jour ses informations 
        si le formulaire soumis est valide, et redirige vers la liste des opérateurs.

        Args:
            request (HttpRequest): L'objet de requête contenant les données du formulaire.
            username (str): Le nom d'utilisateur de l'opérateur à mettre à jour.

        Returns:
            HttpResponse: La réponse qui redirige vers la liste des opérateurs 
                          si le formulaire est valide, sinon retourne le formulaire avec les erreurs.
        """
        # Récupérer l'opérateur à partir de l'username
        operateur = User.objects.get(username=username)
        form = OperateurForm(request.POST, instance=operateur)

        if form.is_valid():
            form.save()  # Sauvegarder les données modifiées
            return redirect('/liste_operateurs_tableau/')  # Rediriger vers la liste des opérateurs

        return render(request, 'assurance/detail_operateur.html', {'form': form, 'operateur': operateur})
    
###############
# region client
###############

class ListeClients(ListView):
    """
    Affiche une liste des utilisateurs ayant le statut 'client' et permet de 
    supprimer un client à partir de son nom d'utilisateur.
    """
    model = User
    template_name = 'assurance/liste_clients_tableau.html'
    context_object_name = 'clients'

    def get_queryset(self):
        """
        Récupère la liste des utilisateurs qui sont marqués comme clients.

        Returns:
            QuerySet: Un ensemble d'objets `User` filtrés avec `is_client = 1`.
        """
        return User.objects.filter(is_client = 1)
    
    def post(self, request):
        """
        Supprime un client à partir de son nom d'utilisateur s'il existe.

        Args:
            request (HttpRequest): L'objet de la requête contenant les données du formulaire (notamment le `username`).

        Returns:
            HttpResponse: Redirection vers la page de liste des clients après suppression.
        """
        username = request.POST.get('username')
        if username:
            client = User.objects.filter(username = username).first()
            if client:
                client.delete()
                return redirect('/liste_clients_tableau')


class EnregistrerClient(CreateView):
    """
    Vue permettant d'enregistrer un nouvel utilisateur avec le rôle 'client'.
    Utilise un formulaire de création pour l'utilisateur et redirige vers la liste des clients 
    après une soumission réussie.
    """
    model = User
    form_class = ClientForm
    template_name = 'assurance/enregistrer_client.html'
    success_url = reverse_lazy('liste_clients')
    

class ModifierCLient(View):
    """
    Vue permettant de modifier les informations d'un client existant.
    Affiche un formulaire pré-rempli avec les données actuelles du client pour modification.
    Si le formulaire est valide, les données sont sauvegardées et l'utilisateur est redirigé
    vers la liste des clients.
    """
    def get(self, request, username):
        """
        Récupère le client en fonction de l'username et affiche le formulaire de modification.
        
        Args:
            request: La requête HTTP.
            username: L'username du client à modifier.
        
        Returns:
            La réponse HTTP avec le formulaire pré-rempli pour le client.
        """
        client = User.objects.get(username=username)
        form = ClientForm(instance=client)
        return render(request, 'assurance/detail_client.html', {'form': form, 'client': client})

    def post(self, request, username):
        """
        Traite la soumission du formulaire de modification et enregistre les données si le formulaire est valide.
        
        Args:
            request: La requête HTTP contenant les données du formulaire.
            username: L'username du client à modifier.
        
        Returns:
            La réponse HTTP avec la redirection vers la liste des clients ou le formulaire de modification si invalide.
        """
        client = User.objects.get(username=username)
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()  
            return redirect('/liste_clients_tableau/')  

        return render(request, 'assurance/detail_client.html', {'form': form, 'client': client})


#################
# region prospect
#################

class EnregistrerProspect(CreateView):
    """
    Vue permettant d'enregistrer un prospect en créant un nouvel utilisateur.
    Affiche un formulaire d'inscription pour un prospect. Lorsque le formulaire est soumis
    et validé, l'utilisateur est créé et redirigé vers la liste des prospects.
    """
    model = User
    form_class = ProspectForm
    template_name = 'assurance/enregistrer_prospect.html'
    success_url = reverse_lazy('liste_prospects')


class ListeProspects(ListView):
    """
    Vue permettant d'afficher une liste des prospects sous forme de tableau.
    Permet également de supprimer un prospect ou de le convertir en client.
    Lors de la soumission d'un formulaire, si un prospect est supprimé, il est supprimé de la base de données.
    Si un prospect est converti en client, ses attributs sont mis à jour pour refléter ce changement.
    """
    model = User
    template_name = 'assurance/liste_prospects_tableau.html'
    context_object_name = 'prospects'

    def get_queryset(self):
        """
        Filtre et retourne uniquement les utilisateurs qui sont des prospects.
        """
        return User.objects.filter(is_prospect = 1)
    
    def post(self, request):
        """
        Traite les demandes de suppression ou de conversion d'un prospect.
        - Si un prospect doit être supprimé, il est effacé de la base de données.
        - Si un prospect doit être converti en client, ses attributs sont mis à jour.
        """
        username_delete = request.POST.get('username_delete')
        print(request.POST)
        if username_delete:
            prospect = User.objects.filter(username = username_delete).first()            
            if prospect:
                prospect.delete()
        username_client = request.POST.get('username_client')
        if username_client:
            prospect = User.objects.filter(username = username_client).first()
            if prospect:
                prospect.is_prospect = False
                prospect.is_client = True
                prospect.save()
        return redirect('/liste_prospects_tableau')
    
    
class ModifierProspect(View):
    """
    Vue permettant de modifier les informations d'un prospect spécifique.
    Lors de la requête GET, le formulaire est pré-rempli avec les informations du prospect.
    Lors de la requête POST, les informations du prospect sont mises à jour si le formulaire est valide.
    """
    def get(self, request, username):
        """
        Récupère les informations du prospect à partir de son `username` et remplit le formulaire avec ces données.
        Affiche le formulaire de modification pour ce prospect.
        """
        prospect = User.objects.get(username=username)
        form = ProspectForm(instance=prospect)
        return render(request, 'assurance/detail_prospect.html', {'form': form, 'prospect': prospect})

    def post(self, request, username):
        """
        Récupère les informations soumises via le formulaire et met à jour le prospect avec ces nouvelles données.
        Si le formulaire est valide, les informations sont sauvegardées et l'utilisateur est redirigé vers la liste des prospects.
        """
        prospect = User.objects.get(username=username)
        form = ProspectForm(request.POST, instance=prospect)
        if form.is_valid():
            form.save()  
            return redirect('/liste_prospects_tableau/')  
        return render(request, 'assurance/detail_prospect.html', {'form': form, 'prospect': prospect})


class ClientProfil(ListView):
    """
    Vue permettant d'afficher et de gérer les informations du profil client.
    La vue affiche les informations de l'utilisateur actuellement connecté.
    Lors de la requête POST, elle permet de mettre à jour le statut de l'utilisateur pour le marquer comme client.
    """
    model = User 
    template_name = 'assurance/page_utilisateur_client.html'
    context_object_name = 'client'  
    
    def get_queryset(self):
        """
        Récupère l'utilisateur actuellement connecté via son `username`.
        Cette méthode permet d'afficher uniquement les informations de l'utilisateur connecté.
        """
        username = self.request.user.username
        return User.objects.filter(username = username)[0]

    def post(self, request, *args, **kwargs):
        """
        Met à jour le statut de l'utilisateur en tant que client.
        Change les attributs `is_client` et `is_prospect` et enregistre la date de souscription.
        Envoie un message de succès et redirige l'utilisateur vers la page de son profil.
        """
        user = self.request.user
        user.is_client = True
        user.is_prospect = False
        user.date_souscription = datetime.datetime.now()
        user.save()
        messages.success(request, "Vous êtes maintenant client!")
        return redirect('page_utilisateur_client')   
    

################
# region contact
################
