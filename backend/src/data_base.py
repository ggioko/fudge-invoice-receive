'''
data base file
'''
import pickle
from datetime import datetime
time = datetime.timestamp(datetime.now())
initial_object = {
    'communication_reports': [],
    # {
    #     'comm_time': dt_string,
    #     'recvd': True,
    #     'invoice_id': invoice_id,
    #     'comm_msg': comm_msg,
    #     'invoice_name': invoice_name
    #     'comm_rep_id': int
    # }


    'invoices': [],
    #   {
    #       'invoice_id': int,
    #       'time_stamp': mon 10th march 3:00pm
    #       'recvd': bool,
    #       "comm_msg": "invoice successfully received maybe error msg",
    #       invoice_name':
    #
    #   }
    'invoices': [],
#   {
#       'invoice_id': int,
#       'invoice_content': bytes,
#       'invoice_name': 
#   }
    #       'invoice_content': bytes,
    #       'invoice_name':
    #   }

    'accounts': [],
    #   {
    #       'email': string,
    #       'password': string,
    #       'comm_reps': [comm_rep_ids],
    #       'u_id': u_id
    #       'username': string
    #
    #   }

    'sessions': [],
    # shouldnt persist session ids
    #   {
    #       'u_id': int,
    #       'session_ids': [str]
    #
    #   }   
    'unreg_emails': [],
    #   {
    #       email: string
    #       comm_reps: [comm_rep_ids]
    #   }

}


class DataBase:
    '''data base class'''

    def __init__(self):
        try:
            with open('data_base.p', 'rb') as file:
                self.__store = pickle.load(file)
        except:
            self.__store = initial_object

    def get(self):
        '''get data base'''
        return self.__store

    def set(self, store):
        '''error if not dictionary'''
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


global data_base
data_base = DataBase()


def save():
    '''persist the data base'''
    db = data_base.get()
    with open('data_base.p', 'wb') as file:
        pickle.dump(db, file)
    data_base.set(db)
