from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from annonces.views import AnnonceDetailView

urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^inscription$', views.inscription, name='inscription'),
    url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
    url(r'^ajout_annonce$', views.ajout_annonce, name='ajout_annonce'),
    url(r'^voir_annonces$', views.voir_annonces, name='voir_annonces'),
    url(r'^(?P<pk>[-\w]+)/$', AnnonceDetailView.as_view(), name='annonce_detail'),
    url(r'^profil$', views.profil, name='profil'),
    url(r'^mesannonces$', views.mesannonces, name='mesannonces'),

]
