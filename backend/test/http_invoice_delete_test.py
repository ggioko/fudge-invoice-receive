from calendar import c
import pytest
from src.config import url
from src.error import InputError
from test.fixtures import register_http, login_http
import requests
import json

def test_invoice_delete(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + '/invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']
    comm_rep_id = response_data1['comm_rep_id']
    data = {'invoice_id': invoice_id}

    response2 = requests.delete(url + 'invoice_delete', params=data, headers={'authorization' :token})

    assert response2.status_code == 200
    response_data2 = response2.json()
    assert response_data2['comm_msg'] == 'invoice successfully deleted'
    assert response_data2['invoice_id'] == invoice_id
    assert response_data2['invoice_name'] == 'example1.xml'


    ## searching for deleted invoice ###
    data = {'invoice_id': invoice_id}
    response3 = requests.get(url + 'search_id', params=data, headers={'authorization' :token})
    assert response3.status_code == 200
    response_data3 = response3.json()
    assert response_data3['comm_msg'] == 'invoice successfully deleted'


    response2 = requests.get(url + 'search_name', params={'invoice_n': 'example1.xml'}, headers={'authorization': token})
    assert response2.status_code == 200
    assert response_data3['comm_msg'] == 'invoice successfully deleted'


    response2 = requests.get(url + 'invoice_content', params=data, headers={'authorization' :token})

    assert response2.status_code == 400


def test_invoice_delete_bad_id(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']
    comm_rep_id = response_data1['comm_rep_id']
    data = {'invoice_id': invoice_id + 10}

    response2 = requests.delete(url + 'invoice_delete', params=data, headers={'authorization' :token})

    assert response2.status_code == 400


def test_invoice_delete_different_account(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']
    comm_rep_id = response_data1['comm_rep_id']
    data = {'invoice_id': invoice_id}

    response1 = requests.post(f'{url}auth_register/', json={'email': 'a@email.com', 'password': 'hello123'})
    response1 = requests.post(f'{url}auth_login/', json={'email': 'a@email.com', 'password': 'hello123'})

    assert response1.status_code == 200
    response_data1 = response1.json()
    token1 = response_data1['token']

    response2 = requests.delete(url + 'invoice_delete', params=data, headers={'authorization' :token1})


    assert response2.status_code == 403


