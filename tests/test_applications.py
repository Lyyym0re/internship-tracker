import asyncio

from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv("app/.env")
client = TestClient(app)

def test_patch(monkeypatch):
    fake_pool = object()
    # noinspection PyUnresolvedReferences
    monkeypatch.setattr(app.state, "db_pool", fake_pool, raising=False)
    with patch("app.api.applications.update_application_status", return_value=
    {"id" : 1, "company" : "w", "position" : "a", "status" : "interview"}) as mock_patch:
        result = client.patch("/applications/1", json={"status" : "interview"})

    assert result.status_code == 200
    mock_patch.assert_awaited_once_with(1, "interview", fake_pool)


def test_all_endpoint():
    with TestClient(app, backend_options={"loop_factory" : asyncio.SelectorEventLoop}) as test_client:
        response_post = test_client.post(
            "/applications",
                json={"company" : "Base company", "position" : "Base position"}
        )
        assert response_post.status_code == 201
        created = response_post.json()

        response_get_id = test_client.get(f"/applications/{created["id"]}")
        assert response_get_id.status_code == 200
        response_get_json = response_get_id.json()
        assert created == response_get_json

        response_patch = test_client.patch(
            f"/applications/{created["id"]}",
            json={"status" : "interview"}
        )
        assert response_patch.status_code == 200
        created["status"] = "interview"
        response_patch_json = response_patch.json()
        assert created == response_patch_json

        response_delete = test_client.delete(f"/applications/{created["id"]}")
        assert response_delete.status_code == 204

        response_get_none = test_client.get(f"/applications/{created["id"]}")
        assert response_get_none.status_code == 404
