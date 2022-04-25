'''file containing functions to generate a communication report'''
import uuid
from datetime import datetime
from src.error import InputError
from src.data_base import data_base

def gen_report(invoice_id, comm_status, invoice_name, u_id):
    '''
    Function for generating a communication report.

    Input:
        invoice_name: string
        invoice_content: string
        comm_status: string

    Output: communication report.

    This generates a communication report based on communication status
    (comm_status). If status is "OK" it returns a communication report with the
    generated invoice id. Otherwise communication report has no invoice id.
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
    recvd = False

    # comm report if error occurs
    communication_report = {
        'comm_time': dt_string,
        'recvd': recvd,
        'comm_msg': comm_status,
        'invoice_name': invoice_name,
        'comm_rep_id': comm_rep_id
    }

    # comm report for no errors
    if comm_status == 'OK':
        comm_msg = "Invoice " + str(invoice_id) + " was successfully uploaded."
        communication_report = {
            'comm_time': dt_string,
            'recvd': True,
            'invoice_id': invoice_id,
            'comm_msg': comm_msg,
            'invoice_name': invoice_name,
            'comm_rep_id': comm_rep_id
        }
    db['communication_reports'].append(communication_report)

    ## link this communication report to the users account
    for account in db['accounts']:
        if account['u_id'] == u_id:
            account['comm_reps'].append(comm_rep_id)
            data_base.set(db)
            return communication_report

    raise InputError(description='no user found')
