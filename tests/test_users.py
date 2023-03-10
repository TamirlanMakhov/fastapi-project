from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.json() == {"message": "welcome to main page"}
    assert response.status_code == 200
