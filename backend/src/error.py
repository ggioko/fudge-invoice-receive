'''file containing http errors'''
from werkzeug.exceptions import HTTPException


class AccessError(HTTPException):
    '''http exception access error'''
    code = 403
    message = 'Access Error: Incorrect token provided'


class InputError(HTTPException):
    '''http exception input error'''
    code = 400
    message = 'Input Error: Document must be UBL'
