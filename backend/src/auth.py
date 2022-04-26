'''
This file contains functions for token generation and checking.
'''
import hashlib
import re
import smtplib
from src.config import NO_RESET_CODE
from src.error import InputError
from src.config import EMAIL, PASSWORD
from src.data_base import data_base
from src.helpers import gen_id, gen_token, gen_session_id
from email.message import EmailMessage


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
    db = data_base.get()
    num = len(db['accounts'])
    username = f'user{num}'
    # store user in data base
    accounts = db['accounts']
    if any(account['email'] == email for account in accounts):
        data_base.set(db)
        raise InputError('an account with this email already exists')
    u_id = gen_id(accounts, 'u_id')
    password = hashlib.sha256((password).encode()).hexdigest()
    comm_reps = []

    # check if email being registered has previously received comm_reps
    # via email receiving
    for entry in  db['unreg_emails']:
        if entry['email'] == email:
            comm_reps = entry['comm_reps']
            db['unreg_emails'].remove(entry)
    account_info = {'email': email, 'password': password, 'comm_reps': comm_reps, 'u_id': u_id, 'username': username, 'reset_code': NO_RESET_CODE}
    
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
    db = data_base.get()
    for session in db['sessions']:
        if session['u_id'] == u_id:
            for s_id in session['session_ids']:
                if s_id == session_id:
                    session['session_ids'].remove(s_id)
    
    return {}

def reset_password_req(email):
    db = data_base.get()
    u_id = -1
    reset_code = NO_RESET_CODE
    for account in db['accounts']:
        if account['email'] == email:
            reset_code = gen_id(db['accounts'], 'reset_code')
            account['reset_code'] = reset_code
            u_id = account['u_id']
            force_logout(u_id)
    data_base.set(db)
    if reset_code == NO_RESET_CODE:
        raise InputError(description='password could not be reset')

    msg = EmailMessage()
    msg.set_content(f'This email contains your one time code to reset your password for your Invoice Platform Account{reset_code}')
    msg['subject'] = 'Invoice Platform Password Reset'
    msg['From'] = EMAIL
    msg['To'] = email
    
    smtp = smtplib.SMTP(host= 'smtp.gmail.com', port=587)
    smtp.starttls()
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(msg)
    smtp.quit
    return {}

def reset_password(reset_code, new_password):
    if len(new_password) < 8:
        raise InputError(description='password must be at least eight characters')
    db = data_base.get()
    for account in db['accounts']:
        if account['reset_code'] == reset_code:
            account['password'] = hashlib.sha256((new_password).encode()).hexdigest()
            account['reset_code'] = NO_RESET_CODE
    data_base.set(db)
    return {}

def force_logout(u_id):
    db = data_base.get()
    for session in db['sessions']:
        if session['u_id'] == u_id:
            session['session_ids'] = []
