from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.utils import timezone
from annonces.forms import UserProfileForm, UserForm, AnnonceForm


from annonces.models import UserProfile, Annonce


def home(request):
    list_profils=[]
    for profil in UserProfile.objects.all():
        list_profils.append(profil)
    profils_dict = {'profils': list_profils, 'annonces': Annonce.objects.all()}

    return render(request, 'annonces/home.html', profils_dict)


def connexion(request):
    """Vue de connexion. Si les informations renseignées sont correctes, connecte l'utilisateur
    et le redirige vers la page d'accueil"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
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
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()  # Sauvegarde de l'entrée utilisateur

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES: # Sauvegarde de la photo de profil si elle existe
                profile.picture = request.FILES['picture']

            profile.ville = request.POST.get('ville')
            profile.numero = request.POST.get('numero')
            profile.region = request.POST.get('region')
            profile.pays = request.POST.get('pays')
            profile.code_postal = request.POST.get('code_postal')
            profile.rue = request.POST.get('rue')
            profile.lat = float(request.POST.get('cityLat'))
            profile.long = float(request.POST.get('cityLng'))

            profile.save()  # Sauvegarde de l'entrée profil
            # Update our variable to tell the template registration was successful.
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
    logout(request)
    return redirect(reverse(connexion))


def ajout_annonce(request):

    # A boolean value for telling the template whether the post was successful.
    # Set to False initially. Code changes value to True when post succeeds.
    posted = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        annonce_form = AnnonceForm(data=request.POST)

        # If the form is valid...
        if annonce_form.is_valid():
            # Save the user's form data, but commit=False doesn't send it right now to the database
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
            # Update our variable to tell the template registration was successful.
            posted = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(annonce_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        annonce_form = AnnonceForm()

    # Render the template depending on the context.
    return render(request, 'annonces/ajout_annonce.html', {'annonce_form': annonce_form, 'posted': posted} )
