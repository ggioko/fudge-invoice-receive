# This file tests the token_check function in src
import pytest
from src.helpers import gen_token, check_token
from src.error import AccessError
from test.fixtures import clear_fixture
from src.data_base import data_base

incorrect_token = 'blahblah'
int_type = 123


# test the correct string token returns a is_valid = True output
def test_correct_token(clear_fixture):

    ## adding dummy data to db to test token generating and encoding
    u_id = 1234
    session_id = '5678'
    db = data_base.get()
    db['accounts'].append(u_id)
    db['sessions'].append({'u_id': u_id})
    for session in db['sessions']:
        if session['u_id'] == u_id:
            session['session_ids'] = []
            session['session_ids'].append(session_id)
    token = gen_token(u_id, session_id)['token']
    check = check_token(token)
    assert u_id == check['u_id']
    assert session_id == check['session_id']


