from fastapi.testclient import TestClient

from app.main import app
from app import schemas

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.json() == {"message": "welcome to main page"}
    assert response.status_code == 200


def test_create_user():
    response = client.post('users', json={"email": "test@mail.ru", "password": "123"})
    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == 'test@mail.ru'
    assert response.status_code == 201
