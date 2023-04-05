from .database import client, session, test_user
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))
    assert res.json().get('message') == 'this is awesome!'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={"email":"h13@gmail.com", 'password':'940202'})
    # this line below is going to do some of the validation for us. it's not going to validate whether the email or password or 
    # other information have correct style. but it's going to check whether the email/password/created_at is given or not. 
    # so this is going to simplify some of the validation process for us, and in continue we can check whether these fields are 
    # correct or not.
    new_user = schemas.Response_User(**res.json())

    assert res.json().get('email') == 'h13@gmail.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
        res = client.post('/login', data={"username": test_user['email'], 'password': test_user['password']})
        # here we wanna check whether out jwt token is valid or not
        login_res = schemas.Token(**res.json())
        payload_data = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
        id: str = payload_data.get("user_id")

        assert res.status_code == 200