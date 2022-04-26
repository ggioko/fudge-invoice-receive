
import requests
from src.config import url
import pytest
from test.fixtures import login_http, register_http

def test_simple_render(login_http): 
    token = login_http['token']
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    response = requests.post(url + 'invoice_render/', json={'xml': invoice_string}, headers={'authorization': token}) 
    assert response.status_code == 200