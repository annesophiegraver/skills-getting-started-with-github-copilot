import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange: rien à préparer, base vide par défaut
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test POST /activities/{activity_name}/signup

def test_signup_activity():
    # Arrange
    activity = "yoga"
    email = "test@example.com"
    # On crée l'activité dans le backend (dictionnaire en mémoire)
    from src import app as app_module
    app_module.activities[activity] = {"participants": []}
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity}"
    # Vérifie que l'utilisateur est bien inscrit
    from src import app as app_module
    assert email in app_module.activities[activity]["participants"]

# Test DELETE /activities/{activity_name}/unregister

def test_unregister_activity():
    # Arrange
    activity = "yoga"
    email = "test@example.com"
    from src import app as app_module
    app_module.activities[activity] = {"participants": [email]}
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Unregistered {email} from {activity}"
    # Vérifie que l'utilisateur n'est plus inscrit
    from src import app as app_module
    assert email not in app_module.activities[activity]["participants"]
