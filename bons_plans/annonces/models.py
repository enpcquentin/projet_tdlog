from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver






class Categorie(models.Model):
    """ Différentes catégorie possibles
    Elles ont été créées à la main via l'interface d'administration Django """

    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom



class Annonce(models.Model):
    """ Modèle d'annonce avec plusieurs attributs """

    titre = models.CharField(max_length=100)
    categorie = models.ForeignKey('Categorie')
    auteur = models.ForeignKey(User)
    descriptif = models.TextField(null=True)
    date = models.DateTimeField()
    numero = models.IntegerField(default=2)
    rue = models.CharField(max_length=100, default='Allée de la Noiseraie')
    pays = models.CharField(max_length=100, default='France')
    code_postal = models.IntegerField(default=77420)
    region = models.CharField(max_length=100, default='Île-de-France')

    ville = models.CharField(max_length=100, default='Noisy-le-Grand')
    lat = models.FloatField(default=48.8411)
    long = models.FloatField(default=2.5880)
    somme_notes = models.IntegerField(default=0)
    nb_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.titre



class UserProfile(models.Model):
    """Modèle de profil, lié à chaque compte utilisateur"""

    # on relie chaque instance UserProfile a une instance de User
    user = models.OneToOneField(User)

    # autres attributs
    website = models.URLField(blank=True)
    numero = models.IntegerField(default=2)
    rue = models.CharField(max_length=100, default='Allée de la Noiseraie')
    pays = models.CharField(max_length=100, default='France')
    code_postal = models.IntegerField(default=77420)
    region = models.CharField(max_length=100, default='Île-de-France')

    picture = models.ImageField(upload_to='static/img', blank=True)
    ville = models.CharField(max_length=100, default='Noisy-le-Grand')
    lat = models.FloatField(default=48.8411)
    long = models.FloatField(default=2.5880)
    annonces_votes = models.ManyToManyField(Annonce)

    def __unicode__(self):
        return self.user.username
