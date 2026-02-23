import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.api import app

@pytest.fixture
def client():
    """Fixture Pytest instanciant un client de test pour Flask"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    """
    Teste que le point de contrôle DevOps du backend retourne un statut normal (200).
    Exigence de l'Enterprise Architecture.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert "camrail-ml-api" in response.json["service"]

def test_predict_bad_method(client):
    """
    Vérifie la robustesse de rebond (Méthodes HTTP interdites).
    """
    response = client.get("/predict")
    # GET n'est pas permis, POST exigé
    assert response.status_code == 405

def test_predict_unauthorized(client):
    """
    Vérifie la sécurité enterprise : Rejet si pas d'API Key.
    """
    response = client.post("/predict", json={})
    assert response.status_code == 401
    assert "error" in response.json

def test_predict_schema_validation(client):
    """
    Vérifie la robustesse Pydantic : Rejet si payload invalide.
    """
    headers = {"X-API-KEY": "entreprise_secret_key_2026"}
    response = client.post("/predict", json={"loco_id": "LOCO_001"}, headers=headers)
    assert response.status_code == 400
    assert "Data Validation Failed" in response.json["error"]
