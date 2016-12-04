from django.contrib import admin
from annonces.models import Categorie, Annonce, UserProfile

admin.site.register(Categorie)
admin.site.register(Annonce)
admin.site.register(UserProfile)