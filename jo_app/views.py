from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormulaireInscription, FormulaireConnexion

# INSCRIPTION
def inscription(request):
    if request.method == 'POST':
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            messages.success(request, "Inscription réussie !")
            return redirect('accueil')  
    else:
        form = FormulaireInscription()
    return render(request, 'jo_app/inscription.html', {'form': form})

# CONNEXION
def connexion_utilisateur(request):
    if request.method == 'POST':
        form = FormulaireConnexion(request, data=request.POST)
        if form.is_valid():
            utilisateur = form.get_user()
            login(request, utilisateur)
            messages.success(request, "Connexion réussie !")
            return redirect('accueil')  
    else:
        form = FormulaireConnexion()
    return render(request, 'jo_app/connexion.html', {'form': form})


def accueil(request):
    return render(request, 'jo_app/accueil.html')

# DÉCONNEXION
def deconnexion_utilisateur(request):
    logout(request)
    messages.info(request, "Déconnexion effectuée.")
    return redirect('connexion')
