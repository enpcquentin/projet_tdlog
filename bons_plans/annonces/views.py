# A nettoyer
from django.http import HttpResponse, Http404
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from annonces.forms import ConnexionForm
from django.contrib.auth.models import User
from annonces.forms import UserCreateForm


def home(request):
    #text="""Bonjour"""
    #return HttpResponse(text)
    return render(request, 'annonces/home.html')


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'annonces/connexion.html', locals())


def inscription(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            email = form.cleaned_data["email"]
            # user = User(username=username,password=password1,email=email)
            form.save(True)
            envoi = True
    else:
        form = UserCreateForm()
    return render(request, 'annonces/inscription.html', locals())




def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))



