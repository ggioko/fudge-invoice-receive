import requests
from src.config import url
from src.auth import register, login
import pytest


@pytest.fixture
def setup():
    requests.delete(url + 'clear/')

def test_register_valid(clear_fixture):
    register('good@email.com', 'hello123')

# test the invoice_search_id function receives the correct communication report when a valid invoice_id is passed.
def test_valid_id(setup):
    data1 = login('good@email.com', 'hello123')
    token = data1['token']

    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']

    data = {'invoice_id': invoice_id}
    response2 = requests.get(url + 'search_id/', params=data, headers={'authorization' :token})
    response_data2 = response2.json()

    assert response2.status_code == 200

    assert response_data2['invoice_id'] == invoice_id
    assert response_data2['recvd'] == True
    assert response_data2['comm_msg'] == "Invoice " + \
        str(invoice_id) + " was successfully uploaded."
    assert response_data2['invoice_name'] == "example1.xml"


def test_invalid_id(setup):
    data1 = login('good@email.com', 'hello123')
    token = data1['token']
    data = {'invoice_id': 1234}
    response2 = requests.get(url + 'search_id/', params=data, headers={'authorization' :token})
    assert response2.status_code == 400


def test_invalid_token(setup):
    data1 = login('good@email.com', 'hello123')
    token = data1['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    data = {'invoice_name': 'example1.xml',
            'invoice_content': invoice_string}
    response1 = requests.post(url + 'invoice_receive', headers={'authorization' :token}, json=data)
    response_data1 = response1.json()

    assert response1.status_code == 200

    invoice_id = response_data1['invoice_id']

    data = {'invoice_id': invoice_id}
    response2 = requests.get(url + 'search_id/', params=data, headers={'authorization' :'wrong_token'})

    # AccessError for invalid token but valid invoice_id
    assert response2.status_code == 403
