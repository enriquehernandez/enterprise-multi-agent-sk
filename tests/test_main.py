# tests/test_main.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


@patch("app.main.run_multi_agent_task")
def test_orchestrate_success(mock_run_task):
    mock_run_task.return_value = "Resultado simulado"  # <-- Sin AsyncMock
    response = client.post("/orchestrate", json={"task": "Escribe un poema"})
    assert response.status_code == 200
    assert response.json() == {"result": "Resultado simulado"}


@patch("app.main.run_multi_agent_task")
def test_orchestrate_failure(mock_run_task):
    mock_run_task.side_effect = Exception("Error simulado")
    response = client.post("/orchestrate", json={"task": "Escribe un poema"})
    assert response.status_code == 500
