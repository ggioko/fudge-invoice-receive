import pytest
from src.config import url
from src.error import InputError
from test.fixtures import register_http, login_http
import requests
import json

def test_login(register_http):
    response = requests.post(f'{url}auth_login/', json={'email': 'good@email.com', 'password': 'hello123'})
    u_id1 = json.loads(response.text)['u_id']
    token = json.loads(response.text)['token']
    assert response.status_code == 200
    response = requests.post(f'{url}auth_login/', json={'email': 'good@email.com', 'password': 'hello123'})
    assert response.status_code == 200
    u_id2 = json.loads(response.text)['u_id']
    token1 = json.loads(response.text)['token']
    assert token != token1
    assert u_id1 == u_id2

def test_login_bad_password(register_http):
    response = requests.post(f'{url}auth_login/', json={'email': 'good@email.com', 'password': 'hello124'})
    assert response.status_code == 400
    
def test_login_bad_email(register_http):
    response = requests.post(f'{url}auth_login/', json={'email': 'good1@email.com', 'password': 'hello123'})
    assert response.status_code == 400

def test_logout_valid(login_http):
    token = login_http['token']
    response = requests.post(f'{url}auth_logout/', headers={'authorization': token})
    assert response.status_code == 200

    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml', 'invoice_content': invoice_string}
    response = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    assert response.status_code == 403

