'''This file contains functions to delete an invoice with a given invoice id'''
from src.data_base import data_base
from src.config import decrypt, key
from src.invoice_search import invoice_search_id
from src.error import InputError, AccessError
from src.comm_report import gen_report
import uuid
from datetime import datetime

def invoice_delete(invoice_id, u_id):
    comm_rep = invoice_search_id(invoice_id, u_id)
    
    ## invoice is in store and user has access to it
    db = data_base.get()
    invoice_name = ''
    found = False
    ## delete from store (delete invoice)
    for invoice in db['invoices']:
        if invoice['invoice_id'] == invoice_id:
            invoice_name = invoice['invoice_name']
            db['invoices'].remove(invoice)
            found = True

    # delete communication report from original invoice so it is no longer accessible
    if found == False:
        raise InputError(description= 'No invoice with this id has been uploaded to the system')

    for account in db['accounts']:
        found == False
        if account['u_id'] == u_id:
            for comm_rep_id in account['comm_reps']:
                if comm_rep_id == comm_rep['comm_rep_id']:
                    found == True
                    account['comm_reps'].remove(comm_rep_id)

    if found == False:
        raise AccessError(description= 'This resource is not accessible to user')

    for comm_reps in db['communication_reports']:
        if comm_reps == comm_rep:
            db['communication_reports'].remove(comm_reps)
                    
    return gen_delete_report(invoice_id, invoice_name, u_id)
## generate new communication report

def gen_delete_report(invoice_id, invoice_name, u_id):
    '''
    Function for generating a communication report for a deleted receipt.

    Input:
        invoice_name: string
        invoice_content: string
        comm_status: string

    Output: communication report.

    This generates a communication report indicatiing the invoice has been deleted.
    '''

    db = data_base.get()
    ### need to generate a communication report id
    comm_reps = db['communication_reports']
    comm_rep_id = uuid.uuid4().int
    while any(comm_rep['comm_rep_id'] == comm_rep_id for comm_rep in comm_reps):
        comm_rep_id = uuid.uuid4().int
    comm_rep_id = comm_rep_id & 0xFFFFFFFF
    time_now = datetime.now()
    dt_string = time_now.strftime("%d/%m/%Y %H:%M:%S")

    # comm report if error occurs
    communication_report = {
        'comm_time': dt_string,
        'recvd': True,
        'comm_msg': 'invoice successfully deleted',
        'invoice_name': invoice_name,
        'comm_rep_id': comm_rep_id,
        'invoice_id': invoice_id
    }

    db['communication_reports'].insert(0,communication_report)

    ## link this communication report to the users account
    for account in db['accounts']:
        if account['u_id'] == u_id:
            account['comm_reps'].append(comm_rep_id)
            data_base.set(db)
            return communication_report

    raise InputError(description='no user found')
