'''file containing configuartion information for the server'''
from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes) -> bytes:
    ''' Function to encrypt input. Src https://stackoverflow.com/questions/
    2490334/simple-way-to-encode-a-string-according-to-a-password'''
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    ''' Function to dencrypt input. Src https://stackoverflow.com/questions/
    2490334/simple-way-to-encode-a-string-according-to-a-password'''
    return Fernet(key).decrypt(token)


port = 8080
url = f"http://localhost:{port}/"

key = open('key.key', 'rb').read()


SECRET = 'djksfjkanfd'

# we can receive invoices via this email address
EMAIL = 'invoicerecvapi@gmail.com'
PASSWORD = 'teamfudge'
