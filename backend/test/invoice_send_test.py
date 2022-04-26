import json
import requests
from src.config import url
import pytest
from test.fixtures import login_http, register_http

def test_valid_invoice(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml', 'invoice_content': invoice_string, 'username': 'user0'}
    response = requests.post(url + 'invoice_send', headers={'authorization' :token}, json=data)
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['recvd'] == True
    assert response_data['invoice_name'] == 'example1.xml'

def test_invalid_invoice(login_http):
    token = login_http['token']
    invoice_file = open('test/example2.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example2.xml', 'invoice_content': invoice_string, 'username': 'user0'}
    response = requests.post(url + 'invoice_send', headers={'authorization' :token}, json=data)
    response_data = response.json()
    
    assert response.status_code == 400

def test_invalid_username(login_http): 
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml', 'invoice_content': invoice_string, 'username': 'not_a_user'}
    response = requests.post(url + 'invoice_send', headers={'authorization' :token}, json=data)
    response_data = response.json()
    
    assert response.status_code == 400 
 