from pydoc import describe
from src.error import InputError
from src.data_base import data_base
from src.auth import force_logout
import hashlib
import re

def reset_email(u_id, email, password):
    db = data_base.get()
    email_format = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if not re.fullmatch(email_format,email):
        raise InputError(description='email is not of valid format')
    if any(account['email'] == email for account in db['accounts']):
        data_base.set(db)
        raise InputError('an account with this email already exists')
    for account in db['accounts']:
        if account['u_id'] == u_id:
            if account['password'] == hashlib.sha256((password).encode()).hexdigest():
                account['email'] = email
                data_base.set(db)
                return {}
    data_base.set(db)
    raise InputError(description='Could not reset email at this time')

def update_username(u_id, username, password):
    db = data_base.get()
    if any(account['username'] == username for account in db['accounts']):
        data_base.set(db)
        raise InputError(description='This user  name is taken')

    for account in db['accounts']:
        if account['u_id'] == u_id:
            if account['password'] == hashlib.sha256((password).encode()).hexdigest():
                account['username'] = username
    data_base.set(db)

def get_username(u_id):
    db = data_base.get()
    for account in db['accounts']:
        if account['u_id'] == u_id:
            data_base.set(db)
            return account['username']
    data_base.set(db)
    raise InputError(description= 'No user could be found') 

def delete_account(u_id, password):
    force_logout(u_id)
    db = data_base.get()
    for account in db['accounts']:
        if account['u_id'] == u_id:
            if account['password'] == hashlib.sha256((password).encode()).hexdigest():
                db['accounts'].remove(account)
            else:
                raise InputError(description= 'incorrect password')
    for session in db['sessions']:
        if session['u_id'] == u_id:
            db['sessions'].remove(session)
