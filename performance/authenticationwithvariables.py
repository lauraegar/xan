import pytest
import requests
import json
from freezegun import freeze_time
from datetime import datetime, timedelta

LOGIN_URL="https://api.matchbook.com/bpapi/rest/security/session"

USERNAME="MANQ625"
PASSWORD="c961g8Iy"
WRONG_USERNAME="MAN12345"
WRONG_PASSWORD="2dnfew)kjdfn"
EMPTY_PASSWORD=""

def secure_a_token():
   payload = {
    "username":USERNAME,
    "password":PASSWORD
   }
   header = {
    'content-type': 'application/json;charset=UTF-8',
    'accept': '*/*'
   }
   response = requests.post(LOGIN_URL, data=json.dumps(payload), headers=header)
   data = response.json()
   return data['session-token']

@pytest.fixture(scope='session')
def secure_a_session():
    session = requests.Session()
    response = session.post(LOGIN_URL, json={"username" : USERNAME, "password": PASSWORD})
    data = response.json()
    assert response.status_code==200
    print(session.cookies.get_dict())
    print(data)
    assert session.cookies.get_dict()
    assert "session-token" in data
    assert "user-id" in data
    return session


def test_username_password_login():
    """Test that login works """
    response = requests.post(LOGIN_URL, json={
        "username": USERNAME,
        "password": PASSWORD
    })

    assert response.status_code == 200
    data = response.json()
    assert "session-token" in data
    assert isinstance(data["session-token"], str)
   
def test_wrong_password_login():
    """Test that login doesn't work if the password is incorrect """
    response = requests.post(LOGIN_URL, json={
        "username": USERNAME,
        "password": WRONG_PASSWORD
    })
   
    print(response)
    data = response.json()    
    assert response.status_code == 400

def test_wrong_username_login():
    """Test that login doesn't work if the password is incorrect """
    response = requests.post(LOGIN_URL, json={
        "username": WRONG_USERNAME,
        "password": PASSWORD
    })
   
    print(response)
    data = response.json()    
    assert response.status_code == 400

def test_login_with_session_token(secure_a_session):
   response = secure_a_session.get(LOGIN_URL)
   assert response.status_code == 200
   assert "session-token" in response.json()
   assert "user-id" in response.json()

def test_token_expires():    
    with freeze_time(datetime.utcnow()) as frozen_time:
        token = secure_a_token()
        header = {
            "accept" : "application/json",
            "Authorization" : "Bearer {secure_a_token}"
         }

        #  simulate 6 hours and 1 second later
        frozen_time.tick(timedelta(hours=6, seconds=1))
        # Token should now be expired
        response = requests.get(LOGIN_URL, headers=header)
        assert response.status_code == 401, "Expected 401 after token expiration"
