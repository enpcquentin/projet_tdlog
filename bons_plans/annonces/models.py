from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Annonce(models.Model):
    titre = models.CharField(max_length=100)
    categorie = models.ForeignKey('Categorie')
    #auteur = models.ForeignKey('Profil')
    descriptif = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, 
                                verbose_name="Date de parution")
    #adresse = 

    def __str__(self):
        return self.titre



