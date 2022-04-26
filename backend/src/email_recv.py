'''Module for receiving invoices via email'''
from datetime import datetime
from email.message import EmailMessage
import email
import smtplib
import imaplib
import getpass
import re
import uuid
from src.data_base import data_base
from src.config import EMAIL, PASSWORD, encrypt, key
from src.invoice_recv import invoice_recv, validate_invoice


SERVER = 'imap.gmail.com'

def email_invoice_recv(attachment, valid):
    '''Function to generate a communication report for invoices received via 
    email without a u_id'''
    time_now = datetime.now()
    comm_time = time_now.strftime("%d/%m/%Y %H:%M:%S")
    
    if valid:
        db = data_base.get()
        invoices = db['invoices']
        invoice_id = invoice_id = uuid.uuid4().int & 0xFFFFFF
        while any(invoice['invoice_id'] == invoice_id for invoice in invoices):
            invoice_id = uuid.uuid4().int & 0xFFFFFF
        invoice_data = encrypt(attachment['invoice_content'].encode(), key)
        invoice_info = {
            'invoice_id': invoice_id,
            'invoice_content': invoice_data,
            'invoice_name': attachment['invoice_name']
        }
        comm_reps = db['communication_reports']
        comm_rep_id = uuid.uuid4().int  & 0xFFFFFFFF
        while any(comm_rep['comm_rep_id'] == comm_rep_id for comm_rep in comm_reps):
                comm_rep_id = uuid.uuid4().int & 0xFFFFFFFF
        comm_rep_info = {
            'comm_time': comm_time,
            'recvd': valid,
            'invoice_id': invoice_id,
            'comm_msg': 'invoice was successfully received via email uploading',
            'invoice_name': attachment['invoice_name'],
            'comm_rep_id': comm_rep_id
        }
        db['invoices'].append(invoice_info)
        db['communication_reports'].append(comm_rep_info)
        data_base.set(db)
        return comm_rep_info

    else:
        comm_rep_id = comm_rep_id = uuid.uuid4().int & 0xFFFFFF
        comm_reps = db['communication_reports']
        comm_rep_id = uuid.uuid4().int  & 0xFFFFFFFF
        while any(comm_rep['comm_rep_id'] == comm_rep_id for comm_rep in comm_reps):
                comm_rep_id = uuid.uuid4().int & 0xFFFFFFFF
        comm_rep_info = {
            'comm_time': comm_time,
            'recvd': valid,
            'comm_msg': 'invoice could not be uploaded at this time, please ensure it is ubl compliant',
            'invoice_name': attachment['invoice_name'],
            'comm_rep_id': comm_rep_id
        }
        db['communication_reports'].append(comm_rep_info)
        data_base.set(db)
        return comm_rep_info

def check_email_acount(to_addrs, valid, attachment):
    comm_rep = email_invoice_recv(attachment, valid)
    comm_rep_id = comm_rep['comm_rep_id']
    db = data_base.get()
    for addr in to_addrs:
        reg = False
        for account in db['accounts']:
            if account['email'] == addr:
                account['comm_reps'].append(comm_rep_id)
                reg = True
        # save unregistered email communication reports for if they register in the future.
        if reg == False:
            found = False
            for entry in db['unreg_emails']:
                if entry['email'] == addr:
                    entry['comm_reps'].append(comm_rep_id)
                    found = True
            if found == False:
                db['unreg_emails'].append({'email': addr, 'comm_reps':[comm_rep_id]})
    data_base.set(db)
    return comm_rep['comm_time']

def get_unread():
    '''function to login and return unread messages'''
    connection = imaplib.IMAP4_SSL(SERVER)
    connection.login(EMAIL, PASSWORD)
    connection.select('inbox', readonly=False)
    result, data = connection.search(None,'UNSEEN')
    return {'connection': connection, 'data': data}

def get_attachments(msg):
    '''function to extract attachments from an email'''
    attachments = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        invoice_name = part.get_filename()

        if bool(invoice_name):
            #write content to file and extract string maybe
            invoice_content = part.get_payload(decode=True)
            invoice_content = invoice_content.decode('utf-8')
            attachments.append({'invoice_content': invoice_content,
            'invoice_name': str(invoice_name)})
    return attachments

def check_email():
    '''Function to search through email inbox'''
    info = get_unread()
    connection = info['connection']
    data = info['data']
    mail_ids= []

    for block in data:
        mail_ids += block.split()

    # now go through each individual email by id
    for mail_id in mail_ids:
        status, data = connection.fetch(mail_id, '(RFC822)')
        for part in data:
            if isinstance(part, tuple):
                # skips header at part[0] and goes straight to content
                message = email.message_from_bytes(part[1])
                attachments = get_attachments(message)
                for attachment in attachments:
                    reply_to_email(message, attachment)

    connection.close()
    connection.logout()


def reply_to_email(message, attachment):
    '''Function to send communication report to client'''
    # reply to email
    email_format = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    recip_types = ['to', 'cc']
    ccd = message['cc']
    to_addrs = []
    # extract all emails invoice should be received to
    for recip_type in recip_types:
        try:
            msg_to = message[recip_type].split()
            for i in range(len(msg_to)):
                msg_to[i] = msg_to[i].replace('<',"").replace('>',"")
                if re.fullmatch(email_format, msg_to[i]) and not(any(email == msg_to[i] for email in to_addrs) and not email == EMAIL):
                    to_addrs.append(msg_to[i].lower())
        except:
            continue
    

    email_to = email.utils.parseaddr(message['from'])[1]
    to_addrs.append(email_to.lower())
    print(f'to: {to_addrs} \n\n\n\n')
    valid = validate_invoice(attachment['invoice_content']) 
    time = check_email_acount(to_addrs, valid, attachment)
    reply = ''
    invoice_name = attachment['invoice_name']
    if valid:
        reply = f'You have received a new invoice on Invoice Receiving Platform, log in or register via our web app to view the communication report.{invoice_name} was \
         received at {time}.'
    else:
        reply = f'An attempt was made to upload an invoice on Invoice Receiving Platform. {invoice_name} could not be processed at {time},  please upload an invoice that complies\
        with Australian ubl standards .'
    for addr in to_addrs:
        msg = EmailMessage()
        msg.set_content(reply)
        msg['subject'] = 'Invoice Receving Platform'
        msg['From'] = EMAIL
        smtp = smtplib.SMTP(host= 'smtp.gmail.com', port=587)
        smtp.starttls()
        smtp.login(EMAIL, PASSWORD)
        msg['To'] = addr  
        m_to = msg['To']
        smtp.send_message(msg)
    smtp.quit
