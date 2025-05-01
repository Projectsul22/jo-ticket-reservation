import pytest
from django.urls import reverse
from django.test import Client
from jo_app.models import Offre

@pytest.mark.django_db
def test_page_accueil_accessible():
    client = Client()
    url = reverse('accueil')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_creation_offre():
    offre = Offre.objects.create(nom_offre="Solo", nombre_places=1, prix=50.00)
    assert offre.nom_offre == "Solo"
    assert offre.prix == 50.00
    assert offre.nombre_places == 1

