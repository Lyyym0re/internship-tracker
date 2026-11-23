from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch


client = TestClient(app)

def test_update_status_application():


    expected = {"id" : 4, "company" : "OOO bank", "position" : "top", "status" : "interview"}
    with patch("app.main.update_application_status", return_value=expected) as mock_update:
        response = client.patch("/applications/4", json={"status" : "interview"})


    assert response.json() == expected
    assert response.status_code == 200
    mock_update.assert_called_once_with(4, "interview")
