import pytest
import requests
from test.fixtures import login_http, register_http
from src.config import SECRET 
from src.config import url
from datetime import datetime
import json
import jwt


def test_invoice_recv_good(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml', 'invoice_content': invoice_string}
    response = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data = response.json()

    assert response_data['comm_time'] == datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S")
    assert response_data['recvd'] == True
    assert response_data['invoice_name'] == 'example1.xml'

    assert response.status_code == 200


def test_invoice_recv_bad(login_http):
    token = login_http['token']
    # example2.xml is an invoice with the incorrect ubl formatting
    invoice_file = open('test/example2.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example2.xml', 'invoice_content': invoice_string}
    response = requests.post(url + 'invoice_receive', headers={'authorization' :token},json=data)
    assert response.status_code == 400

def test_invoice_recv_bad_token(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    ## register another account and try to access previous invoice from this account, should throw access error.
    response = requests.post(f'{url}auth_register/', json={'email': 'good1@email.com', 'password': 'hello123'})
    assert json.loads(response.text) == {}
    assert response.status_code == 200
    fake_token = jwt.encode({'u_id': 123, 'session_id': 1}, SECRET, algorithm='HS256')
    assert fake_token != token
    data = {'invoice_name': 'example1.xml', 'invoice_content': invoice_string}
    response = requests.post(url + 'invoice_receive', json=data, headers={'authorization' :fake_token})
    assert response.status_code == 403
  
