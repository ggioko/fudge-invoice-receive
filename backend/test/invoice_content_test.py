import requests
import json
from src.config import url
import pytest
from test.fixtures import register_http, login_http


def test_invoice_content_valid(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']

    data = {'invoice_id': invoice_id}

    response2 = requests.get(url + 'invoice_content', params=data, headers={'authorization' :token})

    assert response2.status_code == 200
    response_data2 = response2.json()

    assert response_data2 == invoice_string


def test_invalid_id(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']

    data = {'token': token, 'invoice_id': invoice_id + 183624}

    response2 = requests.get(url + 'invoice_content', params=data, headers={'authorization' :token})
    response_data2 = response2.json()

    assert response2.status_code == 400


def test_invalid_token(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']

    ## register another account and try to access previous invoice from this account, should throw access error.
    response = requests.post(f'{url}auth_register/', json={'email': 'good1@email.com', 'password': 'hello123'})
    assert json.loads(response.text) == {}
    assert response.status_code == 200


    response = requests.post(f'{url}auth_login/', json={'email': 'good1@email.com', 'password': 'hello123'})
    assert response.status_code == 200
    token1 =  json.loads(response.text)['token']
    assert token1 != token
    data = {'invoice_id': invoice_id}

    response2 = requests.get(url + 'invoice_content', params=data, headers={'authorization' :token1})

    assert response2.status_code == 403
