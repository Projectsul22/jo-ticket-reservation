from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string

# Create your models here.

# ---------------------------
# UTILISATEUR PERSONNALISÉ
# ---------------------------

class Utilisateur(AbstractUser):
    cle_reservation = models.UUIDField(default=uuid.uuid4, editable=False)
    cle_paiement = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ---------------------------
# OFFRE
# ---------------------------

class Offre(models.Model):
    nom_offre = models.CharField(max_length=50)  # ex : solo, duo, familiale
    nombre_places = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # <-- nouveau champ

    def __str__(self):
        return f"{self.nom_offre} ({self.nombre_places} places - {self.prix}€)"


# ---------------------------
# RÉSERVATION
# ---------------------------

class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reservations')
    offre = models.ForeignKey(Offre, on_delete=models.PROTECT)
    date_reservation = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    statut_paiement = models.BooleanField(default=False)  # True si payé
    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)



    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        super().save(*args, **kwargs)

    def _generate_reference(self):
        return 'RES-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    def __str__(self):
        return f"Réservation #{self.id} - {self.utilisateur}"


# ---------------------------
# BILLET
# ---------------------------

class Billet(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='billets')
    code_qr = models.TextField()
    cle_billet = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Billet #{self.id} - Réservation {self.reservation.id}"