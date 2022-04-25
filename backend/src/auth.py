'''
This file contains functions for token generation and checking.
'''
import hashlib
import re

from src.error import InputError
from src.data_base import data_base
from src.helpers import gen_u_id, gen_token, gen_session_id


def register(email, password):
    '''Function for a user to register an account with invoice receiving API
    Arguments:
        email(string)
        password(string)

    Exceptions:
        InputError - email not of standard email format, password less than 8 chars

    Return Value:
        {}
    '''
    # check email is correct format
    email_format = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if not re.fullmatch(email_format,email):
        raise InputError(description='email is not of valid format')

    if len(password) < 8:
        raise InputError(description='password must be at least eight characters')

    # password has to be at least 8 chars alphanumeric
    #if not (re.fullmatch(r"^[a-zA-Z0-9]$", password)):
    #    raise InputError(description='password must be alphanumeric')

    # should hash the password before storing
    db = data_base.get()
    # store user in data base
    accounts = db['accounts']
    if any(account['email'] == email for account in accounts):
        data_base.set(db)
        raise InputError('an account with this email already exists')
    u_id = gen_u_id(accounts)
    password = hashlib.sha256((password).encode()).hexdigest()
    account_info = {'email': email, 'password': password, 'comm_reps': [], 'u_id': u_id}
    db['accounts'].append(account_info)
    db['sessions'].append({'u_id': u_id, 'session_ids': []})
    data_base.set(db)
    return {}


def login(email, password):
    '''
    This function will login one user based on the email and password
    Argument:
        email, type: string
        password, type: string

    Exceptions:
        InputError: No such email found
        InputError: wrong password

    Return value:
        returns a dictionary with the u_id associated with the given email and
        password, and a new token
        {'u_id': int,
        'token': token}

    '''
    store = data_base.get()

    accounts = store['accounts']
    # if the user have type the correct password and email then return the auth_user_id
    # otherwise raise Input Error
    for account in accounts:
        if account['email'] == email:
            if hashlib.sha256(password.encode()).hexdigest() != account['password']:
                raise InputError(description= 'password is invalid.')
            u_id = account['u_id']

            # Add a new session_id to the user's sessions list
            new_session_id = gen_session_id(u_id)
            # Save the datastore
            data_base.set(store)
            return {
                'u_id': u_id,
                'token': gen_token(u_id, new_session_id)['token']
            }
    raise InputError(description='email is invalid')

def logout(u_id, session_id):
    pass
