'''file with functions implementing invoice searching'''

from src.data_base import data_base
from src.config import decrypt, key
from src.error import InputError, AccessError


def invoice_search_id(invoice_id, u_id):
    '''
    Function to search for communication report in data base by id
    Input:
        invoice_id: int

    Output: communication report dictionary:

        {   'comm_time': dt_string,
            'recvd': True,
            'invoice_id': invoice_id,
            'comm_msg': comm_msg,
            'invoice_name': invoice_name
        }

    Errors: InputError if no invoice with that id was received
            AccessError if account with u_id did not upload this invoice.
    '''

    db = data_base.get()
    comm_reps = db['communication_reports']
    for comm_rep in comm_reps:
        if comm_rep['recvd'] and comm_rep['invoice_id'] == invoice_id:
            if check_account_access(u_id, comm_rep['comm_rep_id']):
                return comm_rep

    data_base.set(db)

    raise InputError(
        description='Input Error, no invoice with this id has been received.')


def invoice_search_name(invoice_name, u_id):
    '''
    Function to search for communication report in data base by invoice name
    Input:
        invoice_name: string

    Output: A list of commuication reports corresponding to that file name,
    including reports for both failed and successful uploads of files with that
    name.

    Errors:
            InputError if an upload attempt was never processed for             invoice_name.
            AccessError if account with u_id did not upload this invoice.
    '''
    db = data_base.get()
    found_reports = []
    comm_reps = db['communication_reports']
    for comm_rep in comm_reps:
        if comm_rep['invoice_name'] == invoice_name:
            for account in db['accounts']:
                if account['u_id'] == u_id:
                    if any (comm_rep_id == comm_rep['comm_rep_id'] for comm_rep_id in account['comm_reps']):
                        found_reports.append(comm_rep)

    data_base.set(db)

    if len(found_reports) == 0:
        description = 'Input Error, no attempt has been made to upload an invoice with this name'
        raise InputError(description=description)

    return found_reports


def get_invoice_data(invoice_id, u_id):
    '''
    Function to search for invoice content in data store by invoice id.
    Input:
        invoice_id: int

    Output:
        invoice_content: string

    Errors: InputError if an invoice with this id was never received.
            AccessError if account with u_id did not upload this invoice.
    '''
    db = data_base.get()
    invoices = db['invoices']
    for invoice in invoices:
        if invoice['invoice_id'] == invoice_id:
            for comm_rep in db['communication_reports']:
                if comm_rep['invoice_id'] == invoice_id:
                    check_account_access(u_id, comm_rep['comm_rep_id'])
                content = decrypt(invoice['invoice_content'], key).decode()
                return content

    raise InputError(description= 'Input Error, no invoice with this id has been received.')
  
def check_account_access(u_id, comm_rep_id):
    '''
    Function check if account with u_id has access to a communication report with given comm_rep_id
    Input:
        u_id: int,
        comm_rep_id: int

    Output:
        True, if comm report found for the given u_id

    Errors: AccessError if account does not have a communication report corresponding to that comm_rep_id.
    '''
    db = data_base.get()
    for account in db['accounts']:
        if account['u_id'] ==  u_id:
            if any(comm_rep == comm_rep_id for comm_rep in account['comm_reps']):
                return True
    raise AccessError(description= 'user does not have permission to access this resource')
    