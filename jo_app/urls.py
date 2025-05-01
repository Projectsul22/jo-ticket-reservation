from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('accueil')),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion_utilisateur, name='connexion'),
    path('accueil/', views.accueil, name='accueil'),
    path('offres/', views.offres, name='offres'),
    path('reserver/<int:offre_id>/', views.reserver_offre, name='reserver_offre'),
    path('payer/<int:reservation_id>/', views.payer_reservation, name='payer'),

    path('deconnexion/', views.deconnexion_utilisateur, name='deconnexion'),
]
