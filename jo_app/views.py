from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormulaireInscription, FormulaireConnexion
from .models import Offre


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

def offres(request):
    offres = Offre.objects.all()
    return render(request, 'jo_app/offres.html', {'offres': offres})


@login_required
def reserver_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    # Ici on peut créer une réservation temporaire, ou afficher les détails à confirmer
    return render(request, 'jo_app/reservation.html', {'offre': offre})

# DÉCONNEXION
def deconnexion_utilisateur(request):
    logout(request)
    messages.info(request, "Déconnexion effectuée.")
    return redirect('connexion')
