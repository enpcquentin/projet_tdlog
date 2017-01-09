from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from annonces.models import UserProfile, Annonce, Categorie


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class AnnonceForm(forms.ModelForm):

    class Meta:
        model = Annonce
        fields = ('titre', 'categorie', 'descriptif')

class VoirAnnonces(forms.ModelForm):

    class Meta:
        model = Annonce
        fields = ('categorie', 'ville')
