import pytest
from jose import jwt
from app import schemas
from app.config import settings


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


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '123', 403),
    ('test@mail.ru', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, '123', 422),
    ('test@mail.ru', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code

