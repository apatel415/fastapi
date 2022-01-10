from jose import jwt
from starlette import status
import pytest
from app.config import settings
from app import schemas


def test_root(client):
    res = client.get('/')
    print(res.json())
    assert res.status_code == 200

def test_create_user(client):
    # have to add the trailing slash because fastapi redirects the post without the trailing slash
    # to with trailing slash, so initially will create a 307 temp redirect then a 201 after
    # this happens because we use prefixes for the routers
    res = client.post('/users/', json={"email": "aj123@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'aj123@gmail.com'

def test_login_user(client, test_user):
    # don't need trailing slash for login because did not use prefix to set up route
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
