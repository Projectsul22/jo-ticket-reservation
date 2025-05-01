from django.contrib import admin
from .models import Offre, Reservation, Billet, Utilisateur
from django.contrib.auth.admin import UserAdmin

admin.site.register(Offre)
admin.site.register(Reservation)
admin.site.register(Billet)
admin.site.register(Utilisateur, UserAdmin)  # Pour personnaliser l'utilisateur
