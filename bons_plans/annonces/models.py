from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
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
