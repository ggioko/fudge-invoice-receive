'''Module for receiving invoices via email'''
from datetime import datetime
from email.message import EmailMessage
import email
import smtplib
import imaplib
from src.config import EMAIL, PASSWORD
from src.invoice_recv import invoice_recv


SERVER = 'imap.gmail.com'

def get_unread():
    '''function to login and return unread messages'''
    connection = imaplib.IMAP4_SSL(SERVER)
    connection.login(EMAIL, PASSWORD)
    connection.select('inbox')
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
            invoice_content = part.get_payload(decode=True)
            attachments.append({'invoice_content': str(invoice_content),
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
        comm_rep = {}
        for part in data:
            if isinstance(part, tuple):
                # skips header at part[0] and goes straight to content
                message = email.message_from_bytes(part[1])
                attachments = get_attachments(message)
                for attachment in attachments:
                    try:
                        comm_rep = invoice_recv(attachment['invoice_name'],
                        attachment['invoice_content'])
                    except:
                        time_now = datetime.now()
                        dt_string = time_now.strftime("%d/%m/%Y %H:%M:%S")

                            # comm report if error occurs
                        comm_rep = {
                            'comm_time': dt_string,
                            'recvd': False,
                            'invoice_name': attachment['invoice_name']
                        }
                    reply_to_email(message, comm_rep)

    connection.close()
    connection.logout()


def reply_to_email(message, comm_rep):
    '''Function to send communication report to client'''
    # reply to email
    email_to = email.utils.parseaddr(message['from'])[1]
    msg = EmailMessage()
    reply = ''
    invoice_name = comm_rep['invoice_name']
    time = comm_rep['comm_time']
    if comm_rep['recvd']:
        invoice_id = comm_rep['invoice_id']
        reply = f'Thank you for using invoice receiving API,{invoice_name} was \
         received at {time}. The invoice has been assigned the invoice id: \
         {invoice_id}.'
    else:
        reply = f'Thank you for using invoice receiving API.    {invoice_name} \
        could not be processed at {time}, please upload an invoice containing \
        a ubl specification.'
    msg.set_content(reply)
    msg['subject'] = 'Invoice Receving API'
    msg['From'] = EMAIL
    msg['To'] = email_to

    smtp = smtplib.SMTP(host= 'smtp.gmail.com', port=587)
    smtp.starttls()
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(msg)
    smtp.quit
