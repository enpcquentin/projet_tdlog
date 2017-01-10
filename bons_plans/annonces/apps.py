from django.apps import AppConfig


class AnnoncesConfig(AppConfig):
    """ Application principale de notre site. Elle permet de :
    - poster des annonces portant sur des bons plans tels que des ballades, des services, des échanges ou des restaurants
    - visualiser sur une carte les différentes annonces poster
    - chercher des annonces en fonction de leur catégorie ou de leur ville """
    
    name = 'annonces'
