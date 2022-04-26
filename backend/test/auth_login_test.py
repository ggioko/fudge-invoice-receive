import pytest
from test.fixtures import clear_fixture, register_account
import re
from src.auth import login
from src.error import InputError

def test_login_simple(clear_fixture, register_account): 
    login('good@email.com', 'hello123')

def test_login_different_sessions(clear_fixture, register_account):
    data1 = login('good@email.com', 'hello123')
    data2 = login('good@email.com', 'hello123')
    assert data1['u_id'] == data2['u_id']
    assert data1['token'] != data2['token']

# account was registered in fixtures using email: 'good@email.com' and password: 'hello123'
def test_incorrect_password(clear_fixture, register_account):
    with pytest.raises(InputError):
        data = login('good@email.com', 'hello124')

def test_incorrect_email(clear_fixture, register_account):
    with pytest.raises(InputError):
        data = login('wrong@email.com', 'hello123')