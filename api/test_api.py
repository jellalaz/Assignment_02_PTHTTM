"""
Automated Test Suite for Unified FastAPI Server
Tests all prediction endpoints and health check within the lifespan context.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"]["diabetes"] is True
    assert data["models_loaded"]["house_price"] is True
    assert data["models_loaded"]["ecommerce"] is True


def test_predict_diabetes_high_risk(client):
    payload = {
        "gender": "Female",
        "age": 68.0,
        "hypertension": 1,
        "heart_disease": 1,
        "smoking_history": "current",
        "bmi": 36.5,
        "HbA1c_level": 8.0,
        "blood_glucose_level": 240
    }
    response = client.post("/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 1
    assert "Diabetic" in data["diagnosis"]
    assert 0.0 <= data["probability"] <= 1.0


def test_predict_diabetes_low_risk(client):
    payload = {
        "gender": "Male",
        "age": 22.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "bmi": 21.0,
        "HbA1c_level": 5.1,
        "blood_glucose_level": 85
    }
    response = client.post("/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 0
    assert "Non-Diabetic" in data["diagnosis"]
    assert data["probability"] < 0.5


def test_predict_house_price(client):
    payload = {
        "Area": 3200,
        "Bedrooms": 4,
        "Bathrooms": 3,
        "Stories": 2,
        "Parking": 2,
        "Age": 5,
        "City": "Mumbai",
        "Furnishing": "Furnished",
        "Main Road": "Yes",
        "Guest Room": "Yes",
        "Basement": "No",
        "Water Supply": "Corporation",
        "Air Conditioning": "Yes",
        "Preferred Tenant": "Family",
        "Locality Rating": 8
    }
    response = client.post("/predict/house", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 300000
    assert "$" in data["formatted_price"]
    assert data["currency"] == "USD"


def test_predict_ecommerce_positive(client):
    payload = {
        "Age": 30,
        "Rating": 5,
        "Positive Feedback Count": 5,
        "Division Name": "General",
        "Department Name": "Dresses",
        "Class Name": "Dresses",
        "Review Text": "In love with this dress! Super comfortable and high quality."
    }
    response = client.post("/predict/ecommerce", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommended"] == 1
    assert "Recommended" in data["recommendation_label"]
    assert data["confidence"] > 0.5


def test_predict_ecommerce_negative(client):
    payload = {
        "Age": 45,
        "Rating": 1,
        "Positive Feedback Count": 2,
        "Division Name": "General Petite",
        "Department Name": "Tops",
        "Class Name": "Knits",
        "Review Text": "Terrible material, fell apart in the first wash. Very disappointed."
    }
    response = client.post("/predict/ecommerce", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommended"] == 0
    assert "Not Recommended" in data["recommendation_label"]
    assert data["confidence"] < 0.5
