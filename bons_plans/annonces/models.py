from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Modèle de profil, lié à chaque compte utilisateur"""
    # On relie chaque instance UserProfile a une instance de User
    user = models.OneToOneField(User)

    # Autres attributs
    website = models.URLField(blank=True)
    numero = models.IntegerField(default=2)
    rue = models.CharField(max_length=100, default='Allée de la Noiseraie')
    pays = models.CharField(max_length=100, default='France')
    code_postal = models.IntegerField(default=77420)
    region = models.CharField(max_length=100, default='Île-de-France')

    picture = models.ImageField(upload_to='profile_images', blank=True)
    ville = models.CharField(max_length=100, default='Noisy-le-Grand')
    lat = models.FloatField(default=48.8411)
    long = models.FloatField(default=2.5880)

    def __unicode__(self):
        return self.user.username


# différentes catégorie possibles
# peut être les créer à la main via l'interface d'administration ?
class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


# modèle d'annonce avec plusieurs attributs
class Annonce(models.Model):
    titre = models.CharField(max_length=100)
    categorie = models.ForeignKey('Categorie')
    auteur = models.ForeignKey(User)
    descriptif = models.TextField(null=True)
    date = models.DateTimeField()
    adresse = models.CharField(max_length=100, default = '')
    ville = models.CharField(max_length=20, default = '')
    code_postal = models.CharField(max_length=5, default = '')

    def __str__(self):
        return self.titre
