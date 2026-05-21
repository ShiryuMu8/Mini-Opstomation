# Fichier de tests automatiques pour l'API mini-Opstomation
# Pytest va exécuter toutes les fonctions qui commencent par "test_"
# Dans la CI GitHub Actions, si un test échoue → le déploiement est bloqué

import pytest
from app import app, incidents

# On configure Flask en mode test
# Ça désactive certaines fonctionnalités inutiles pendant les tests
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ===== TESTS DE LA ROUTE /health =====

def test_health_retourne_200(client):
    # On vérifie que l'API répond bien
    # Chez Adeo : Kubernetes ping /health pour savoir si le service est vivant
    response = client.get("/health")
    assert response.status_code == 200

def test_health_retourne_status_ok(client):
    # On vérifie que le contenu de la réponse est correct
    data = response = client.get("/health").get_json()
    assert data["status"] == "ok"
    assert data["service"] == "mini-opstomation"

# ===== TESTS DE LA ROUTE /incidents =====

def test_incidents_retourne_200(client):
    # On vérifie que la liste des incidents est accessible
    response = client.get("/incidents")
    assert response.status_code == 200

def test_incidents_retourne_une_liste(client):
    # On vérifie que la réponse est bien une liste d'incidents
    data = client.get("/incidents").get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_incidents_contient_les_bons_champs(client):
    # On vérifie que chaque incident a bien les champs attendus
    data = client.get("/incidents").get_json()
    for incident in data:
        assert "id" in incident
        assert "service" in incident
        assert "status" in incident
        assert "message" in incident

# ===== TESTS DE LA ROUTE /fix =====

def test_fix_repare_un_incident_en_erreur(client):
    # On vérifie que la réparation automatique fonctionne
    # C'est le coeur d'Opstomation : détecter une erreur et la corriger
    response = client.post("/fix/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["incident"]["status"] == "fixed"

def test_fix_incident_inexistant_retourne_404(client):
    # On vérifie qu'un incident inexistant retourne une erreur 404
    response = client.post("/fix/999")
    assert response.status_code == 404

def test_fix_incident_deja_ok(client):
    # On vérifie qu'un incident déjà ok ne change pas de statut
    response = client.post("/fix/3")
    data = response.get_json()
    assert data["incident"]["status"] == "ok"