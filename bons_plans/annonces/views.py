from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.views.generic.detail import DetailView
from annonces.forms import UserProfileForm, UserForm, AnnonceForm, VoirAnnonces
from annonces.models import UserProfile, Annonce


def home(request):
    """ Page d'accueil """

    list_profils=[]
    for profil in UserProfile.objects.all():
        list_profils.append(profil)
    profils_dict = {'profils': list_profils, 'annonces': Annonce.objects.order_by('date').reverse()}

    return render(request, 'annonces/home.html', profils_dict)


def connexion(request):
    """Vue de connexion. Si les informations renseignées sont correctes, connecte l'utilisateur
    et le redirige vers la page d'accueil"""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            # on vérifie que le compte courant est valide et actif
            # si c'est le cas, on connecte l'utilisateur
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/annonces/home')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'annonces/connexion.html', {})



def inscription(request):
    """Vue d'inscription qui enregistre l'entrée utilisateur, l'entrée profil et les relie entre eux"""

    # un booléan pour tester la validation de l'enregistrement
    registered = False

    # on a besoin d'une méthode POST pour le formulaire
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            # sauvegarde de l'entrée utilisateur
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                # sauvegarde de la photo de profil si elle existe
                profile.picture = request.FILES['picture']

            profile.ville = request.POST.get('ville')
            profile.numero = request.POST.get('numero')
            profile.region = request.POST.get('region')
            profile.pays = request.POST.get('pays')
            profile.code_postal = request.POST.get('code_postal')
            profile.rue = request.POST.get('rue')
            profile.lat = float(request.POST.get('cityLat'))
            profile.long = float(request.POST.get('cityLng'))
            # sauvegarde de l'entrée profil
            profile.save()
            # on signale au template que l'enregistrement s'est correctement réalisé
            registered = True
        else:
            print( user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'annonces/inscription.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def deconnexion(request):
    """ Vue de déconnexion """

    logout(request)
    return redirect(reverse(connexion))


def ajout_annonce(request):
    """ Vue pour ajouter une annonce """

    # un booléen pour tester la validation de la demande
    posted = False

    # on a besoin d'une méthode POST pour le formulaire
    if request.method == 'POST':
        annonce_form = AnnonceForm(data=request.POST)
        # on teste la validité du formulaire
        if annonce_form.is_valid():
            # commit = False pour ne pas sauvegarder dans la BDD tout de suite
            annonce = annonce_form.save(commit=False)
            annonce.auteur = request.user
            annonce.date = timezone.now()
            annonce.ville = request.POST.get('ville')
            annonce.numero = request.POST.get('numero')
            annonce.region = request.POST.get('region')
            annonce.pays = request.POST.get('pays')
            annonce.code_postal = request.POST.get('code_postal')
            annonce.rue = request.POST.get('rue')
            annonce.lat = float(request.POST.get('cityLat'))
            annonce.long = float(request.POST.get('cityLng'))
            annonce.save()
            # on signale au template que l'ajout s'est correctement passé
            posted = True
        else:
            print(annonce_form.errors)
    else:
        annonce_form = AnnonceForm()

    return render(request, 'annonces/ajout_annonce.html', {'annonce_form': annonce_form, 'posted': posted} )


def voir_annonces(request):
    """ Vue pour rechercher des annonces par attributs """

    # un booléen pour tester la validation de la demande
    test = False

    if request.method == 'POST':
        form = VoirAnnonces(data=request.POST)
        # on teste la validité du formulaire
        if form.is_valid():
            # commit = False pour ne pas sauvegarder dans la BDD
            # on ne souhaite pas crée un nouvel élément dans la BDD mais juste l'interroger
            cat = form.save(commit = False)
            test = True
            categorie = cat.categorie
            ville = cat.ville
            # interrogation de la BDD
            annonces = Annonce.objects.filter(categorie = categorie, ville = ville)
        else:
            print(form.errors)
    # cas en pratique jamais atteint
    else:
        form = VoirAnnonces()
        annonces = Annonce.objects.all()
        ville = ""
        categorie = ""

    return render(request, 'annonces/voir_annonces.html', {'form': form, 'annonces': annonces, 'test': test, 'ville': ville, 'categorie': categorie})


class AnnonceDetailView(DetailView):
    """ Vue pour n'afficher qu'une annonce en particulier de la BDD, grâce au clés primaires """

    model = Annonce

    def get_context_data(self, **kwargs):
        context = super(AnnonceDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
