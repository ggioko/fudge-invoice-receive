
'''File containing server routes'''
from cgitb import reset
import sys
import time
import threading
from json import dumps
from urllib import response
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from src.auth import register, login, logout, reset_password_req, reset_password
from src.data_base import save
from src.invoice_recv import invoice_recv, clear
from src.invoice_search import invoice_search_id, invoice_search_name, get_invoice_data
from src.helpers import check_token
from src import config
from src.email_recv import check_email
from src.invoice_delete import invoice_delete
import requests
from src.invoice_send import invoice_send
from src.accounts import reset_email, update_username, get_username, delete_account

#sys.stdout = sys.stderr = open('log.txt','a')

app = Flask(__name__)
# this line is for access control issues
cors_config = {
    "origins": "*",
    "methods": ["OPTIONS", "GET", "POST", "DELETE"],
    "allow_headers": ["Authorization", "Content-Type"]
}

CORS(app, resources={
    r"/*": cors_config
})

def email_recv():
    '''function to check every 5 seconds for invoices received via email'''
    while True:
        check_email()
        save()
        time.sleep(20)




def error_handler(err):
    '''function for http error handling'''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        # change this to return communication report instead
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


# handle rrors
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.register_error_handler(Exception, error_handler)


@app.route('/invoice_receive/', methods=['POST'])
def invoice_receive():
    '''route for invoice receiving'''
    data = request.get_json()
    token = request.headers.get('authorization')
    # check if token c(orrect
    user = check_token(token)
    u_id = int(user['u_id'])
    comm_report = invoice_recv(data['invoice_name'], data['invoice_content'], u_id)
    save()
    return jsonify(comm_report)


@app.route('/auth_register/', methods=['POST'])
def register_user():
    # send an email when they register for an account
    '''route for register for an account'''
    data = request.get_json()
    email = data['email']
    password = data['password']
    info = (register(email, password))
    save()
    return jsonify(info)

@app.route('/auth_login/', methods=['POST'])
def login_user():
    '''route for register for an account'''
    data = request.get_json()
    email = data['email']
    password = data['password']
    info = (login(email, password))
    return jsonify(info)

@app.route('/auth_logout/', methods=['POST'])
def logout_user():
    '''route to logout from a session'''
    token = request.headers.get('authorization')
    # check if token c(orrect
    user = check_token(token)
    u_id = int(user['u_id'])
    session_id = user['session_id']
    info = logout(u_id, session_id)
    save()
    return jsonify(info)

@app.route('/auth_reset_password_req/', methods=['POST'])
def password_req():
    # send an email when they register for an account
    '''route for resetting an accounts password'''
    data = request.get_json()
    email = data['email']
    info = reset_password_req(email)
    save()
    return jsonify(info)

@app.route('/auth_reset_password/', methods=['POST'])
def password_reset():
    # send an email when they register for an account
    '''route for resetting an accounts password'''
    data = request.get_json()
    new_password = data['new_password']
    reset_code = int(data['reset_code'])
    info = reset_password(reset_code, new_password)
    save()
    return jsonify(info)

@app.route('/reset_email/', methods=['POST'])
def email_reset():
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    # send an email when they register for an account
    '''route for resetting an accounts password'''
    data = request.get_json()
    email= data['email']
    password = data['password']
    print(f'details: {email}, {password} \n\n\n')
    info = reset_email(int(user['u_id']), email, password)
    save()
    return jsonify(info)

@app.route('/update_username/', methods=['POST'])
def username_update():
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    # send an email when they register for an account
    '''route for resetting an accounts password'''
    data = request.get_json()
    username= data['username']
    print(f'username: {username}\n\n\n')
    password = data['password']
    info = update_username(int(user['u_id']), username, password)
    save()
    return jsonify(info)

@app.route('/search_id', methods=['GET'])
def invoice_search_by_id():
    '''route for searching invoice by id'''
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    u_id = int(user['u_id'])
    invoice_id = int(request.args.get('invoice_id'))
    return jsonify(invoice_search_id(invoice_id, u_id))

@app.route('/username', methods=['GET'])
def find_username():
    '''get username'''
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    u_id = int(user['u_id'])
    info = get_username(u_id)
    save()
    return jsonify({'username': info})



@app.route('/invoice_content', methods=['GET'])
def invoice_data():
    '''route for retreiving invoice content from invoice id'''
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    u_id = int(user['u_id'])
    invoice_id = int(request.args.get('invoice_id'))
    return jsonify(get_invoice_data(invoice_id, u_id))

@app.route('/search_name', methods=['GET'])
def invoice_by_search_name():
    '''route for searching invoice by name'''
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    u_id = int(user['u_id'])
    invoice_name = request.args.get('invoice_n')
    return jsonify(invoice_search_name(invoice_name, u_id))

# clears out the database
@app.route('/clear/', methods=['DELETE'])
def http_clear():
    '''
    Resets the internal data of the application to its initial state.

    Arguments:
        None

    Return Value:

        Returns {} (empty dictionary)
    '''
    clear()
    return {}

@app.route('/invoice_delete', methods=['DELETE'])
def delete_invoices():
    '''
    Deletes an invoice with the given invoice_id

    Arguments:
        invoice_id: int
        token: token
    
    Return Value:
        Returns communication report

    '''
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    u_id = int(user['u_id'])
    invoice_id = int(request.args.get('invoice_id'))
    return jsonify(invoice_delete(invoice_id, u_id))

@app.route('/invoice_render/', methods=['POST'])
def invoice_render(): 
    token = request.headers.get('authorization')
    # check if token correct
    check_token(token)
    resp = request.get_json()
    response = requests.post('https://www.invoicerendering.com/einvoices?renderType=pdf&lang=en', files=resp)
    with open('test.pdf', "wb") as f:
        f.write(response.content)
    return send_file('../test.pdf', mimetype='application/pdf')

@app.route('/invoice_send/', methods=['POST'])
def send_invoice():
    '''route for sending/receiving invoices between accounts
    Arguments: 
        invoice_name: string
        invoice_content: string
    Return: 
        Communication report
    '''
    data = request.get_json()
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    u_id = int(user['u_id'])
    username = data['username']
    comm_report = invoice_send(data['invoice_name'], data['invoice_content'], u_id, username)
    save()
    return jsonify(comm_report)

@app.route('/delete_account', methods=['DELETE'])
def account_delete():
    '''
    Deletes an invoice with the given invoice_id

    Arguments:
        invoice_id: int
        token: token
    
    Return Value:
        Returns communication report

    '''
    token = request.headers.get('authorization')
    # check if token correct
    user = check_token(token)
    password = request.args.get('password')
    u_id = int(user['u_id'])
    delete_account(u_id, password)
    save()
    return {}


if __name__ == '__main__':
    background_tasks = threading.Thread(target=email_recv, daemon=True)
    background_tasks.start()
    app.run(port=config.port, threaded=True)
