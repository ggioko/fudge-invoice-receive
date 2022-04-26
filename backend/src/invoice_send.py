from src.invoice_recv import invoice_check
from src.invoice_recv import invoice_check, invoice_recv
from src.comm_report import gen_report
from src.data_base import data_base
from src.error import InputError

'''
	Function used for one user to send another user an invoice. 

	Input: 
		invoice_name: string
		invoice_content: string
		u_id: int 
		recipient_id: int 

	Output: - Communication Report (dictionary):
		{
			'comm_time': string,
            'recvd': boolean,
            'invoice_id': int,
            'comm_msg': string,
            'invoice_name': string,
            'comm_rep_id': int
		}

'''

def invoice_send(invoice_name, invoice_content, u_id, username): 
	db = data_base.get()
	found = False
	recip_id = -1
	for account in db['accounts']:
		if account['username'] == username:
			recip_id = account['u_id']
	if recip_id == -1:
		raise InputError(description='No user with this username exists')
	invoice_id = invoice_check(invoice_name, invoice_content, recip_id)
	invoice_recv(invoice_name, invoice_content, recip_id)
	return gen_report(invoice_id, 'SENT',  invoice_name, u_id)


