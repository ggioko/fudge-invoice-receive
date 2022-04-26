import json
import requests
from src.config import url
import pytest
from test.fixtures import login_http, register_http


@pytest.fixture
def setup():
    requests.delete(url + 'clear/')


def test_valid_invoice_good(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', json=data, headers={'authorization': token})
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']

    data = {'invoice_n': 'example1.xml'}

    response2 = requests.get(url + 'search_name', headers={'authorization': token}, params=data)
    response_data2 = response2.json()

    assert response2.status_code == 200

    assert response_data2[0]['invoice_id'] == invoice_id
    assert response_data2[0]['recvd'] == True
    assert response_data2[0]['invoice_name'] == "example1.xml"


def test_invalid(login_http):
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive/', json=data, headers={'authorization': token})

    assert response1.status_code == 200

    data = {'invoice_n': 'incorrectname'}
    response2 = requests.get(url + 'search_name', params=data, headers={'authorization': token})
    assert response2.status_code == 400


def test_valid_invbad(login_http):
    token = login_http['token']
    invoice_file = open('test/example2.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example2.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', json=data, headers={'authorization': token})

    assert response1.status_code == 400

    data1 = {'invoice_n': 'example2.xml'}

    response2 = requests.get(url + 'search_name', params=data1, headers={'authorization': token})

    assert response2.status_code == 200


def test_valid_no_name(login_http):
    token = login_http['token']
    # this name does not exist in the system at all
    invoice_file = open('test/example2.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example2.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', json=data, headers={'authorization': token})

    assert response1.status_code == 400

    data1 = {'invoice_n': 'example3.xml'}

    response2 = requests.get(url + 'search_name', params=data1, headers={'authorization': token})

    assert response2.status_code == 400