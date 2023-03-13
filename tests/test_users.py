import pytest
from jose import jwt
from app import schemas
from app.config import settings
from .database import client, session


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@mail.ru", "password": "123"}
    response = client.post('/users/', json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']

    return new_user


def test_root(client):
    response = client.get('/')
    assert response.json() == {"message": "welcome to main page"}
    assert response.status_code == 200


def test_create_user(client):
    response = client.post('/users/', json={"email": "test@mail.ru", "password": "123"})
    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == 'test@mail.ru'
    assert response.status_code == 201


def test_login_user(test_user, client):
    response = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**response.json())  # validating

    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    my_id: str = payload.get('user_id')

    assert my_id == test_user['id']
    assert response.status_code == 200
    assert login_response.token_type == 'bearer'
