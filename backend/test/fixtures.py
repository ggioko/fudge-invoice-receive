import pytest
from src.config import url, SECRET
from src.invoice_recv import clear, invoice_recv
from src.error import InputError
from src.auth import register
from src.data_base import data_base
import requests
import json

@pytest.fixture
def clear_fixture():
    clear()

@pytest.fixture
def dummy_data(clear_fixture):
    u_id = 1234
    session_id = '5678'
    user_info = {'email': 'email@email.com',
           'password': 'password',
           'comm_reps': [],
           'u_id': u_id}
  
    db = data_base.get()
    db['accounts'].append(user_info)
    db['sessions'].append({'u_id': u_id})
    for session in db['sessions']:
        if session['u_id'] == u_id:
            session['session_ids'] = []
            session['session_ids'].append(session_id)
    data_base.set(db)
    return {'u_id': u_id, 'session_id': session_id}

@pytest.fixture
def add_file_good(dummy_data):
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    return invoice_recv('example1.xml', invoice_string, dummy_data['u_id'])
    
@pytest.fixture
def add_file_bad(dummy_data):
    with pytest.raises(InputError):
        invoice_file = open('test/example2.xml', 'r')
        invoice_string = invoice_file.read()
        return invoice_recv('example2.xml', invoice_string, dummy_data['u_id'])

@pytest.fixture
def register_account():
    register('good@email.com', 'hello123')

@pytest.fixture
def register_http():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'good@email.com', 'password': 'hello123'})
    assert response.status_code == 200

@pytest.fixture
def login_http(register_http):
    response = requests.post(f'{url}auth_login/', json={'email': 'good@email.com', 'password': 'hello123'})
    assert response.status_code == 200
    return json.loads(response.text)
    
