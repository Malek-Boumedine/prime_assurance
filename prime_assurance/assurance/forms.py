from django import forms
from .models import User, RendezVous
from django.forms import ModelForm
import pandas as pd
from datetime import datetime
import cloudpickle



# region ouverture model
with open('assurance/basic_linreg_model.pkl', 'rb') as file:
    model_pred = cloudpickle.load(file)
    """
    Charge un modèle d'apprentissage automatique à partir d'un fichier pickle.

    Cette méthode ouvre le fichier `basic_linreg_model.pkl` contenant un modèle préalablement sauvegardé 
    et le charge en mémoire à l'aide de la bibliothèque `cloudpickle`. Le modèle peut ensuite être utilisé 
    pour effectuer des prédictions.

    Lève :
        Exception : Si une erreur se produit lors de l'ouverture ou du chargement du fichier, une exception est levée.
    """


# region login
class LoginForm(forms.Form):
    """
    Formulaire de connexion pour les utilisateurs.

    Ce formulaire permet aux utilisateurs de saisir leur nom d'utilisateur 
    et leur mot de passe pour se connecter à l'application.

    Attributs :
        username (CharField) : Champ pour le nom d'utilisateur, limité à 150 caractères.
        password (CharField) : Champ pour le mot de passe, limité à 150 caractères, affiché sous forme de champ de type mot de passe.
    """
    username = forms.CharField(max_length=150, label='Nom d’utilisateur')
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Mot de passe')
    

# region rendez-vous
class RendezVousForm(forms.ModelForm):
    """
    Formulaire pour la création ou la modification d'un rendez-vous.

    Ce formulaire permet aux utilisateurs de renseigner les informations nécessaires 
    pour prendre un rendez-vous, incluant la date, l'heure, et l'opérateur. 
    Il effectue également une validation pour vérifier qu'aucun rendez-vous n'existe déjà 
    à la même date et heure pour le même opérateur.

    Attributs :
        date (DateField) : Champ pour la date du rendez-vous.
        heure (ChoiceField) : Champ pour l'heure du rendez-vous, avec des plages horaires pré-définies.
    """
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    heure = forms.ChoiceField(choices=[
        ('09:00', '09:00 - 09:30'),
        ('09:30', '09:30 - 10:00'),
        ('10:00', '10:00 - 10:30'),
        ('10:30', '10:30 - 11:00'),
        ('11:00', '11:00 - 11:30'),
        ('11:30', '11:30 - 12:00'),
        ('14:00', '14:00 - 14:30'),
        ('14:30', '14:30 - 15:00'),
        ('15:00', '15:00 - 15:30'),
        ('15:30', '15:30 - 16:00'),
        ('16:00', '16:00 - 16:30'),
        ('16:30', '16:30 - 17:00'),
        ('17:00', '17:00 - 17:30'),
        ('17:30', '17:30 - 18:00'),
    ])    
    class Meta:
        """
        Métadonnées pour le formulaire `RendezVousForm`.

        Définit le modèle associé (RendezVous) et les champs à inclure dans le formulaire.

        Attributs :
            model (RendezVous) : Le modèle lié à ce formulaire, ici `RendezVous`.
            fields (list) : Liste des champs à inclure dans le formulaire.
        """        
        model = RendezVous
        fields = ['prenom','nom', 'motif', 'operateur', 'type']
    
    def clean(self):
        """
        Valide les données soumises par l'utilisateur.

        Cette méthode vérifie si un rendez-vous existe déjà pour l'opérateur à la date et 
        l'heure demandées. Si tel est le cas, elle lève une exception de validation.

        Retourne :
            dict : Les données nettoyées (date_heure ajoutée si valide).
        
        Lève :
            ValidationError : Si un rendez-vous existe déjà pour l'opérateur à la date et l'heure spécifiées.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        heure = cleaned_data.get('heure')
        operateur = cleaned_data.get('operateur')
        
        if date and heure and operateur:
            heure_obj = datetime.strptime(heure, '%H:%M').time()
            date_heure = datetime.combine(date, heure_obj)

            # Vérifier si un rendez-vous existe déjà
            if RendezVous.objects.filter(operateur=operateur, date_heure=date_heure).exists():
                raise forms.ValidationError("Ce créneau est déjà pris pour cet opérateur. Veuillez choisir un autre horaire.")

            cleaned_data['date_heure'] = date_heure
        return cleaned_data

    def save(self, commit=True):
        """
        Sauvegarde le rendez-vous dans la base de données.

        Cette méthode crée une instance du modèle `RendezVous` à partir des données nettoyées 
        et l'enregistre dans la base de données. Si les champs date et heure sont définis, 
        elle combine ces informations dans un champ `date_heure`.

        Arguments :
            commit (bool) : Si True, l'instance sera immédiatement sauvegardée. Par défaut, True.
        
        Retourne :
            RendezVous : L'instance du rendez-vous sauvegardée.
        """
        instance = super().save(commit=False)
        date = self.cleaned_data.get('date')
        heure = self.cleaned_data.get('heure')
        if date and heure:
            heure_obj = datetime.strptime(heure, '%H:%M').time()
            instance.date_heure = datetime.combine(date, heure_obj)
        if commit:
            instance.save()
        return instance    


# region opérateur
class OperateurForm(ModelForm):
    """
    Formulaire pour la création ou la modification d'un opérateur.

    Ce formulaire permet de gérer les informations nécessaires à la création d'un opérateur, 
    y compris ses informations personnelles, son poste, et son mot de passe. Il vérifie également 
    la correspondance des mots de passe et définit l'utilisateur comme un opérateur après la validation.

    Attributs :
        sexe (ChoiceField) : Champ pour le sexe de l'opérateur (Homme ou Femme).
        region (ChoiceField) : Champ pour la région de l'opérateur (Northwest, Northeast, Southwest, Southeast).
        poste (ChoiceField) : Champ pour le poste de l'opérateur (Courtier ou Manager).
        password (CharField) : Champ pour le mot de passe de l'opérateur.
        confirm_password (CharField) : Champ pour la confirmation du mot de passe.
    """
    sexe = forms.ChoiceField(required=True, choices=[('male', 'Homme'), ('female', 'Femme')])
    region = forms.ChoiceField(required=True, choices=[('northwest', 'Northwest'), ('northeast', 'Northeast'), ('southwest', 'Southwest'), ('southeast', 'Southeast')])
    poste = forms.ChoiceField(required=True, choices=[('courtier', 'Courtier'), ('manager', 'Manager')])
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirmer le mot de passe')

    class Meta:
        """
        Métadonnées pour le formulaire `OperateurForm`.

        Définit le modèle associé (User) et les champs à inclure dans le formulaire.
        Configure également les widgets pour certains champs, notamment pour afficher
        le champ `date_de_naissance` sous un format de saisie de date HTML.

        Attributs :
            model (User) : Le modèle lié à ce formulaire, ici `User`.
            fields (list) : Liste des champs à inclure dans le formulaire.
            widgets (dict) : Dictionnaire des widgets à utiliser pour certains champs.
        """
        model = User
        fields = ['first_name','last_name','sexe','username','password','confirm_password','email','date_de_naissance','telephone','anciennete','poste']
        widgets = {
            'date_de_naissance': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})}

    def clean(self):
        """
        Valide la correspondance des mots de passe.

        Cette méthode vérifie que les mots de passe saisis et leur confirmation sont identiques.
        
        Retourne :
            dict : Les données nettoyées.
        
        Lève :
            ValidationError : Si les mots de passe ne correspondent pas.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return cleaned_data

    def save(self, commit=True):
        """
        Sauvegarde l'opérateur dans la base de données.

        Cette méthode crée un utilisateur, définit son mot de passe, et le marque comme opérateur. 
        L'utilisateur est ensuite enregistré dans la base de données.

        Arguments :
            commit (bool) : Si True, l'utilisateur est immédiatement sauvegardé. Par défaut, True.
        
        Retourne :
            User : L'instance de l'utilisateur opérateur sauvegardé.
        """
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        user.is_operateur = True
        if commit:
            user.save()
        return user
    

# region modifier profil
class ModifierProfilForm(ModelForm):
    """
    Formulaire pour la modification du profil utilisateur.

    Ce formulaire permet à l'utilisateur de mettre à jour ses informations personnelles, 
    telles que son nom, son sexe, sa région, et d'autres détails pertinents pour son profil.
    """
    class Meta:
        """
        Métadonnées pour le formulaire `ModifierProfilForm`.

        Définit le modèle associé (User) et les champs à inclure dans le formulaire 
        pour la modification du profil utilisateur.

        Attributs :
            model (User) : Le modèle lié à ce formulaire, ici `User`.
            fields (list) : Liste des champs à inclure dans le formulaire.
        """
        model = User
        fields = ['first_name','last_name','sexe','region','statut_fumeur','nombre_enfant','email','date_de_naissance','telephone','poids','taille']


# region modifier opérateur
class OperateurModification(ModelForm):
    """
    Formulaire pour la modification des informations d'un opérateur.

    Ce formulaire permet de mettre à jour les informations personnelles et professionnelles 
    d'un opérateur, telles que son nom, son prénom, son sexe, son poste, etc.

    Attributs :
        model (User) : Le modèle associé à ce formulaire, ici `User`.
        fields (list) : Liste des champs à inclure dans le formulaire.
        widgets (dict) : Dictionnaire des widgets à utiliser, notamment pour le champ `date_de_naissance`.
    """
    model = User
    fields = ['first_name','last_name','sexe','username','email','date_de_naissance','telephone','poste']
    widgets = {'date_de_naissance': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})}
    

# region client
class ClientForm(ModelForm):
    """
    Formulaire pour la création ou la modification d'un client.

    Ce formulaire permet à un client de s'enregistrer ou de modifier ses informations personnelles,
    y compris des détails sur son statut fumeur, sa région, son poids, sa taille, et son mot de passe.
    Il effectue également une validation des mots de passe et calcule l'IMC du client à partir des 
    informations fournies.

    Attributs :
        sexe (ChoiceField) : Champ pour le sexe du client (Homme ou Femme).
        region (ChoiceField) : Champ pour la région du client (Northwest, Northeast, Southwest, Southeast).
        statut_fumeur (ChoiceField) : Champ pour le statut fumeur (Oui ou Non).
        first_name (CharField) : Champ pour le prénom du client.
        password (CharField) : Champ pour le mot de passe du client.
        confirm_password (CharField) : Champ pour confirmer le mot de passe.
    """
    sexe = forms.ChoiceField(required=True, choices=[('male', 'Homme'), ('female', 'Femme')])
    region = forms.ChoiceField(required=True, choices=[('northwest', 'Northwest'), ('northeast', 'Northeast'), ('southwest', 'Southwest'), ('southeast', 'Southeast')])
    statut_fumeur = forms.ChoiceField(choices=[('yes', 'Oui'), ('no', 'Non')])
    first_name = forms.CharField(required=True, label='Prénom')
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirmer le mot de passe')

    class Meta:
        """
        Métadonnées pour le formulaire `ClientForm`.

        Définit le modèle associé (User) et les champs à inclure dans le formulaire pour la création 
        ou la modification d'un client. Configure également les widgets pour certains champs, 
        notamment pour afficher le champ `date_de_naissance` sous un format de saisie de date HTML.

        Attributs :
            model (User) : Le modèle lié à ce formulaire, ici `User`.
            fields (list) : Liste des champs à inclure dans le formulaire.
            widgets (dict) : Dictionnaire des widgets à utiliser, notamment pour le champ `date_de_naissance`.
        """
        model = User
        fields = ['first_name','last_name','username','sexe','region','statut_fumeur','nombre_enfant','password','confirm_password','email','date_de_naissance','telephone','poids','taille']
        widgets = {'date_de_naissance': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})}

    def clean(self):
        """
        Valide la correspondance des mots de passe.

        Cette méthode vérifie que les mots de passe saisis et leur confirmation sont identiques.

        Retourne :
            dict : Les données nettoyées.

        Lève :
            ValidationError : Si les mots de passe ne correspondent pas.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return cleaned_data

    def save(self, commit=True):
        """
        Sauvegarde le client dans la base de données.

        Cette méthode crée ou met à jour un utilisateur client, calcule son IMC en fonction 
        de son poids et de sa taille, et prédit ses charges d'assurance à l'aide d'un modèle externe.
        Si le mot de passe est défini, il est haché avant d'être sauvegardé. 

        Arguments :
            commit (bool) : Si True, l'utilisateur est immédiatement sauvegardé. Par défaut, True.

        Retourne :
            User : L'instance de l'utilisateur client sauvegardée.
        """
        # Récupérer l'instance de l'utilisateur avant d'ajouter le hachage
        user = super().save(commit=False)

        #éviter l'erreur des champs vides
        if user.poids is not None and user.taille is not None:
            if user.poids > 0 and user.taille >0 :
                user.imc = user.poids / ((user.taille /100) ** 2)

        # Si le mot de passe a été modifié, hachage avec SHA-256
        if self.cleaned_data.get('password'):
            password = self.cleaned_data['password']
            user.set_password(password)  # Utilise le hashage sécurisé de Django
            user.age = datetime.now().year - user.date_de_naissance.year
            user.is_client = True
            user.is_prospect = False

            # #faire un dataframe pour model
            df_pour_model = pd.DataFrame([[user.age, user.sexe,user.imc,user.nombre_enfant,user.statut_fumeur,user.region]], columns=['age','sex','bmi','children','smoker','region'])
            print(df_pour_model)
            print(df_pour_model.dtypes)

            with open('assurance/basic_linreg_model.pkl', 'rb') as file:
                model_pred = cloudpickle.load(file)
            charge = model_pred.predict(df_pour_model)
            print(charge)
            print(charge[0])
            user.charges = charge[0]

        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        return user
    

# region prospect
class ProspectForm(ClientForm):
    """
    Formulaire pour la création ou la modification d'un prospect.

    Ce formulaire permet à un prospect de s'enregistrer ou de modifier ses informations personnelles.
    Il hérite des champs du formulaire `ClientForm`, calcule l'IMC et prédit les charges d'assurance 
    pour le prospect en utilisant un modèle externe.

    Attributs :
        Hérite des attributs de `ClientForm` (sexe, région, statut fumeur, etc.).
    """
    class Meta(ClientForm.Meta):
        """
        Métadonnées pour le formulaire `ProspectForm`.

        Hérite des métadonnées du formulaire `ClientForm` et définit le modèle associé 
        (User) ainsi que les champs à inclure dans le formulaire pour la création ou la modification d'un prospect. 
        Configure également les widgets, notamment pour afficher le champ `date_de_naissance` sous un format de saisie de date HTML.

        Attributs :
            model (User) : Le modèle lié à ce formulaire, ici `User`.
            fields (list) : Liste des champs à inclure dans le formulaire.
            widgets (dict) : Dictionnaire des widgets à utiliser, notamment pour le champ `date_de_naissance`.
        """
        model = User
        fields = ['first_name','last_name','username','sexe','region','statut_fumeur','nombre_enfant','password','confirm_password','email','date_de_naissance','telephone','poids','taille']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'})}

    def save(self, commit=True):
        """
        Sauvegarde le prospect dans la base de données.

        Cette méthode crée ou met à jour un utilisateur prospect, calcule son IMC, 
        prédit ses charges d'assurance à l'aide d'un modèle externe, et définit l'utilisateur 
        comme prospect dans le système.

        Arguments :
            commit (bool) : Si True, l'utilisateur est immédiatement sauvegardé. Par défaut, True.

        Retourne :
            User : L'instance de l'utilisateur prospect sauvegardée.
        """
        user = super(ClientForm, self).save(commit=False)

        if user.poids is not None and user.taille is not None:
            if user.poids > 0 and user.taille > 0:
                user.imc = user.poids / ((user.taille /100) ** 2)

        if self.cleaned_data.get('password'):
            password = self.cleaned_data['password']
            user.set_password(password)  # Utilise le hashage sécurisé de Django
            user.age = datetime.now().year - user.date_de_naissance.year
            user.is_prospect = True
            user.is_client = False
            df_pour_model = pd.DataFrame([[user.age, user.sexe,user.imc,user.nombre_enfant,user.statut_fumeur,user.region]], columns=['age','sex','bmi','children','smoker','region'])

            with open('assurance/basic_linreg_model.pkl', 'rb') as file:
                model_pred = cloudpickle.load(file)
            charge = model_pred.predict(df_pour_model)
            user.charges = charge[0]
        # Sauvegarder l'utilisateur
        if commit:
            user.save()
        return user    


# region devis
class DevisForm(ClientForm):
    """
    Formulaire pour la création d'un devis d'assurance.

    Ce formulaire permet à un utilisateur de renseigner ses informations personnelles 
    pour obtenir un devis d'assurance. Il hérite du formulaire `ClientForm`, exclut les champs 
    de mot de passe et de confirmation de mot de passe, et ajoute une méthode pour calculer 
    un devis en fonction des informations de l'utilisateur, comme son IMC et son âge.

    Attributs :
        Hérite des attributs de `ClientForm` (nom, prénom, email, etc.).
    """
    password = None
    confirm_password = None
    
    class Meta(ClientForm.Meta):
        """
        Métadonnées pour le formulaire `DevisForm`.

        Hérite des métadonnées du formulaire `ClientForm` et définit le modèle associé 
        (User) ainsi que les champs à inclure dans le formulaire pour la création d'un devis d'assurance. 
        Configure également les widgets, notamment pour afficher le champ `date_de_naissance` sous un format de saisie de date HTML.

        Attributs :
            model (User) : Le modèle lié à ce formulaire, ici `User`.
            fields (list) : Liste des champs à inclure dans le formulaire.
            widgets (dict) : Dictionnaire des widgets à utiliser, notamment pour le champ `date_de_naissance`.
        """
        model = User
        fields = ['last_name', 'first_name', 'email', 'telephone', 'date_de_naissance', 'sexe', 'taille', 'poids', 'nombre_enfant', 'statut_fumeur', 'region']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'})
        }

    def calculer(self):
        """
        Calcule le montant du devis d'assurance en fonction des informations de l'utilisateur.

        Cette méthode calcule l'IMC et l'âge de l'utilisateur, puis utilise un modèle externe 
        pour prédire le montant du devis. Si une erreur survient lors du calcul, elle est gérée.

        Retourne :
            float ou None : Le montant du devis prédit par le modèle, ou None en cas d'erreur.
        """
        user = super().save(commit=False)

        if user.poids and user.taille:
            user.imc = user.poids / ((user.taille/100) ** 2)
            
        if user.date_de_naissance:
            user.age = datetime.now().year - user.date_de_naissance.year
        
        df_pour_model = pd.DataFrame([[user.age, user.sexe, user.imc, user.nombre_enfant, user.statut_fumeur, user.region]], columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])

        try:
            with open('assurance/basic_linreg_model.pkl', 'rb') as file:
                model = cloudpickle.load(file)
            montant = model.predict(df_pour_model)[0]
            return montant
        except Exception as e:
            print(f"Erreur lors du calcul : {e}")
            return None
    

# region  contact
class ContactForm(forms.Form):
    """
    Formulaire de contact permettant aux utilisateurs d'envoyer un message.

    Champs :
        nom (CharField) : Champ pour le nom de l'expéditeur (max 100 caractères).
        email (EmailField) : Champ pour l'adresse e-mail de l'expéditeur.
        message (CharField) : Champ pour le message, affiché sous forme de zone de texte.
    """
    nom = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    