from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormulaireInscription, FormulaireConnexion
from django.utils.crypto import get_random_string
from .models import Offre, Reservation, Billet
import uuid
import qrcode
from io import BytesIO
import base64

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


@login_required
def payer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)

    # Vérifie si déjà payé
    if reservation.statut_paiement:
        return render(request, 'jo_app/billet.html', {'billet': reservation.billets.first()})

    # Génère une clé de paiement unique
    request.user.cle_paiement = uuid.uuid4()
    request.user.save()

    reservation.statut_paiement = True
    reservation.montant = reservation.offre.prix
    reservation.save()

    # Clé définitive = cle_reservation + cle_paiement
    cle_billet = str(request.user.cle_reservation) + str(request.user.cle_paiement)

    # Génère le QR code
    qr = qrcode.make(cle_billet)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    billet = Billet.objects.create(
        reservation=reservation,
        cle_billet=uuid.uuid4(),
        code_qr=image_base64
    )

    return render(request, 'jo_app/billet.html', {'billet': billet})

# DÉCONNEXION
def deconnexion_utilisateur(request):
    logout(request)
    messages.info(request, "Déconnexion effectuée.")
    return redirect('connexion')
