
'''This file contains helper functions for generating tokens and ids'''
import uuid
import jwt
from src.error import AccessError, InputError
from src.config import SECRET
from src.data_base import data_base

def check_token(token):
    '''
    Function to check if token is correct

    Arguments:
       token (string)           - the token to validate and extract auth_id from
    Return Value:
        {'u_id': u_id, 'session_id': session_id} if token is
        valid

    Returns session id to be used on backend for things like logging out
    '''
    decode_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    #extact info
    u_id = int(decode_token['u_id'])
    session_id = decode_token['session_id']
    db = data_base.get()
    # if both userid and session id are valid
    for session in db['sessions']:
        if session['u_id'] == u_id:
            if any(s_id == session_id for s_id in session['session_ids']):
                return {'u_id': u_id, 'session_id': session_id}

    raise AccessError(description='Could not give acccess to user')

def gen_token(u_id, session_id):
    '''
    Function to create a token

    Arguments:
        u_id (integer)   - id of user token is being generated for
    Return Value
        Returns {token}
    '''
    token = jwt.encode({'u_id': u_id, 'session_id': session_id}, SECRET, algorithm= 'HS256')

    return {'token': token}

def gen_session_id(u_id):
    '''
    Function to generate session id when a user logs in (used for token generation)
    '''
    db = data_base.get()
    for session in db['sessions']:
        if session['u_id'] == u_id:
            session_id = str(uuid.uuid4())
            while any(s_id == session for s_id in session['session_ids']):
                session_id = str(uuid.uuid4())
            session['session_ids'].append(session_id)
            return session_id
    raise InputError(description='no user with this id found')

def gen_id(accounts, key):
    '''Function to generate user id for an account'''
    u_id = uuid.uuid4().int
    while any(account[key] == u_id for account in accounts):
        u_id = uuid.uuid4().int
    return u_id & 0xFFFFFFFF
