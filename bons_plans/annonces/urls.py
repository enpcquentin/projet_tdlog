from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^inscription$', views.inscription, name='inscription'),
    url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
]

