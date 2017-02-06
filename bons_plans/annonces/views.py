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

    deja_vote = False
    if request.method == 'POST':
        note = int(request.POST.get('mark'))
        cle = int(request.POST.get('key'))
        if request.user.is_authenticated:
            profile = request.user.userprofile
            for e in profile.annonces_votes.all():
                if e.id==cle:
                    deja_vote = True
            if deja_vote==False:
                add = Annonce.objects.get(id__iexact=cle)
                add.somme_notes += note
                add.nb_votes += 1
                add.save()
                profile.annonces_votes.add(add)
    list_profils=[]
    for profil in UserProfile.objects.all():
        list_profils.append(profil)
    profils_dict = {'profils': list_profils, 'annonces': Annonce.objects.order_by('date').reverse(), 'deja_vote': deja_vote}

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
            if user.is_active and not(user.is_superuser):
                login(request, user)
                return HttpResponseRedirect('/annonces/home')
            else:
                return HttpResponse("Vous n'êtes autorisé à vous connecter.")
        else:
            print("Erreur dans le mot de passe ou l'identifiant : {0}, {1}".format(username, password))
            return HttpResponse("Erreur dans le mot de passe ou l'identifiant.")

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

            profile = profile_form.save(commit=False)
            
            if 'picture' in request.FILES:
                # sauvegarde de la photo de profil si elle existe
                profile.picture = request.FILES['picture']
            try:
                profile.ville = request.POST.get('ville')
                profile.numero = request.POST.get('numero')
                profile.region = request.POST.get('region')
                profile.pays = request.POST.get('pays')
                profile.code_postal = request.POST.get('code_postal')
                profile.rue = request.POST.get('rue')
                profile.lat = float(request.POST.get('cityLat'))
                profile.long = float(request.POST.get('cityLng'))
                # sauvegarde de l'entrée profil
                user.save()
                profile.user = user
                profile.save()
                # on signale au template que l'enregistrement s'est correctement réalisé
                registered = True
            except:
                user.delete()
                return render(request,
                  'annonces/inscription.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': False,'adresse_incorrecte': True})
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'annonces/inscription.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,'adresse_incorrecte': False})


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
            try: 
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
            except:
                return render(request, 'annonces/ajout_annonce.html', {'annonce_form': annonce_form, 'posted': False, 'adresse_incorrecte': True} )
        else:
            print(annonce_form.errors)
    else:
        annonce_form = AnnonceForm()
    return render(request, 'annonces/ajout_annonce.html', {'annonce_form': annonce_form, 'posted': posted, 'adresse_incorrecte': False} )


def profil(request):
    """ Visualisation du profil de l'utilisateur connecté, s'il n'est pas admin """

    modified = False
    profile = request.user.userprofile
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save(commit=False)
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.ville = request.POST.get('ville')
            profile.numero = request.POST.get('numero')
            profile.region = request.POST.get('region')
            profile.pays = request.POST.get('pays')
            profile.code_postal = request.POST.get('code_postal')
            profile.rue = request.POST.get('rue')
            profile.lat = float(request.POST.get('cityLat'))
            profile.long = float(request.POST.get('cityLng'))

            profile.save()
            modified = True
        else:
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        if profile.picture:
            pic_url = '../' + profile.picture.url
        else:
            pic_url = ''
    # Renvoit le template prenant en compte les differents cas
    return render(request,
                  'annonces/profil.html',
                  {'pic_url': pic_url, 'profile_form': profile_form, 'modified': modified})


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
            ville = request.POST.get('ville')
            print(ville)
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
    """ Vue pour n'afficher qu'une annonce en particulier de la BDD, grâce aux clés primaires """

    model = Annonce

    def get_context_data(self, **kwargs):
        context = super(AnnonceDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def mesannonces(request):
    """ Vue pour afficher les annonces de l'utilisateur connecté. Possibilité de les supprimer. """

    utilisateur = request.user
    if request.method == 'POST':
        for add in Annonce.objects.all():
            cle = request.POST.get(str(add.id))
            if cle!=None:
                add.delete()
    mesannonces = Annonce.objects.filter(auteur = utilisateur)
    return render(request,'annonces/mesannonces.html',{'mesannonces': mesannonces})
