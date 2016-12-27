from django.test import TestCase


from annonces.models import Annonce

class AnnonceTestCase(TestCase):
    def test_annonce_possede_categorie(self):
        """Assure que toute annonce possède bien une catégorie"""
        for add in Annonce.objects.all():
            self.assertIsNotNone(add.categorie)

    
    