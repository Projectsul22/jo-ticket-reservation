from PIL import Image as PILImage
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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from django.http import FileResponse
import io

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

    if request.method == 'POST':
        reservation = Reservation.objects.create(
            utilisateur=request.user,
            offre=offre,
            montant=offre.prix,
            statut_paiement=False  # à true plus tard si paiement simulé
        )
        return redirect('payer_reservation', reservation_id=reservation.id)

    return render(request, 'jo_app/reservation.html', {'offre': offre})



@login_required
def payer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)

    if request.method == 'POST' and not reservation.statut_paiement:
        reservation.statut_paiement = True
        reservation.save()

        # Générer la clé de sécurité
        cle_secrete = str(reservation.utilisateur.cle_reservation) + str(reservation.utilisateur.cle_paiement)

        # Générer le QR Code
        qr = qrcode.make(cle_secrete)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Enregistrer le billet
        Billet.objects.create(
            reservation=reservation,
            code_qr=img_base64
        )

        return redirect('qr_code', reservation_id=reservation.id)

    return render(request, 'jo_app/paiement.html', {'reservation': reservation})

@login_required
def qr_code(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    billet = reservation.billets.first()
    return render(request, 'jo_app/qr_code.html', {'billet': billet})

@login_required
def mes_billets(request):
    billets = Billet.objects.filter(reservation__utilisateur=request.user)
    return render(request, 'jo_app/mes_billets.html', {'billets': billets})


@login_required
def telecharger_billet(request, billet_id):
    billet = get_object_or_404(Billet, id=billet_id, reservation__utilisateur=request.user)

    # Générer le QR code à partir de la clef sécurisée
    cle_complete = f"{billet.reservation.utilisateur.cle_reservation}{billet.reservation.utilisateur.cle_paiement}"
    qr_img = qrcode.make(cle_complete)
    qr_img_pil = qr_img.convert("RGB")  # Convertir en image RGB compatible

    # Générer le PDF avec ReportLab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Texte
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 770, "🎫 Billet pour les JO 2024")
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Nom : {billet.reservation.utilisateur.first_name} {billet.reservation.utilisateur.last_name}")
    p.drawString(100, 710, f"Offre : {billet.reservation.offre.nom_offre}")
    p.drawString(100, 690, f"Nombre de places : {billet.reservation.offre.nombre_places}")

    # ✅ Intégrer le QR code depuis l'image PIL
    p.drawInlineImage(qr_img_pil, 100, 500, width=150, height=150)

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='billet_jo2024.pdf')

# DÉCONNEXION
def deconnexion_utilisateur(request):
    logout(request)
    messages.info(request, "Déconnexion effectuée.")
    return redirect('connexion')
