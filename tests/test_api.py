import os

os.environ["DEMO_MODE"] = "true"

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["demo_mode"] is True


def test_generate_demo_document():
    payload = {
        "document_type": "NDA",
        "parties": "Alice (Disclosing Party), Example Ltd (Receiving Party)",
        "terms": "Confidentiality; No disclosure to third parties",
        "effective_date": "2026-09-22",
        "jurisdiction": "Not specified",
        "additional_instructions": "",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["demo_mode"] is True
    assert "NDA" in body["content"]
