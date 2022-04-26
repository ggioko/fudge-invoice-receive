'''file containing functions for invoice receiving and processing'''
import uuid
import os
import time
import requests
from src.data_base import data_base
from src.config import key, encrypt, EMAIL, PASSWORD
from src.comm_report import gen_report
from src.error import InputError


def clear():
    '''function to clear the data store'''
    db = data_base.get()
    db['invoices'].clear()
    db['communication_reports'].clear()
    db['accounts'].clear()
    db['sessions'].clear()
    if os.path.exists('data_base.p'):
        os.remove('data_base.p')
    return {}


def invoice_recv(invoice_name, invoice_content, u_id):
    '''
    Function for recieving invoice information and generating a communication report.
    Input:
        invoice_name: string
        invoice_content: string

    Output: dictionary: 'comm_time': dt_string,
            'recvd': True,
            'invoice_id': invoice_id,
            'comm_msg': comm_msg,
            'invoice_name': invoice_name
        }

    This function add the invoice to the data store if it is UBL. Otherwise the
    function raises an InputError.

    '''
    invoice_id = invoice_check(invoice_name, invoice_content, u_id)

    # call communication report generation function
    return gen_report(invoice_id, 'OK',  invoice_name, u_id)


def invoice_check(invoice_name, invoice_content, u_id):
    '''
    Function for checking invoice has UBL version in its content

    Input:
        invoice_name: string
        invoice_content: string

    Output: dictionary: {'code': int, 'invoice_id': int}

    This function processes the invoice data and generates a unique invoice id.
    The invoice_info is stored in the data base, if it has a UBL version line,
    otherwise and InputError is raised.
    '''

    # unassigned invoice id until invoice passes check

    # quick validation check for input, must be ubl
    if not validate_invoice(invoice_content):
        raise InputError(description=gen_report(-1, 400, invoice_name, u_id))

     # generate unique invoice id
    db = data_base.get()
    invoices = db['invoices']
    invoice_id = invoice_id = uuid.uuid4().int & 0xFFFFFF
    while any(invoice['invoice_id'] == invoice_id for invoice in invoices):
        invoice_id = uuid.uuid4().int & 0xFFFFFF
    # encypt the invoice data, rather than just storing plain text
    invoice_data = encrypt(invoice_content.encode(), key)
    # only store invoice if correct input
    invoice_info = {'invoice_content': invoice_data,
                    'invoice_id': invoice_id, 'invoice_name': invoice_name}
    db['invoices'].append(invoice_info)

    data_base.set(db)

    return invoice_id

def validate_invoice(invoice_content):
    if not ('<cbc:UBLVersionID>' in invoice_content and'</cbc:UBLVersionID>' in invoice_content):
        return False
    return True

    #info = {'email': EMAIL, 'password': '123!hello', 'name_first': 'invoice', #'name_last': 'recv'}
    #requests.post('https://go-apple-pie.herokuapp.com/auth/register', #json=info) 
#
#
    #info = {'email': EMAIL, 'password': '123!hello'}
    #response = requests.post('https://go-apple-pie.herokuapp.com/auth/login', #json=info)
    #while response.status_code != 200:
    #    response = requests.post('https://go-apple-pie.herokuapp.com/auth/#login', json=info)   
    #token = response.json()['token']
#
    #info = {'email': EMAIL, 'password': '123!hello'}
    #response = requests.post(f'https://go-apple-pie.herokuapp.com/invoice/#validate?token={token}', invoice_content)
    #print(response)
    #if response.status_code == 200:
    #    return True
    #return False
    