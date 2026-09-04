from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "finmirror-ai-api"
    assert body["status"] == "running"


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_metrics_endpoint_exposed() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
