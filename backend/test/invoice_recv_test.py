import pytest
import json
from src.invoice_recv import invoice_check
from src.data_base import data_base
from test.fixtures import clear_fixture, dummy_data
from src.error import InputError


def test_check_invoice_good(dummy_data):
    # test that good file is added to data base
    u_id = dummy_data['u_id']
    db = data_base.get()
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    invoice_check('example1.xml', invoice_string, u_id)
    assert len(db['invoices']) == 1
    data_base.set(db)

def test_check_invoice_bad(dummy_data):
    with pytest.raises(InputError):
        u_id = dummy_data['u_id']
        # test bad file raises input and is not added to data base
        invoice_file = open('test/example2.xml', 'r')
        invoice_string = invoice_file.read()
        invoice_check('example2.xml', invoice_string, u_id)
        db = data_base.get()
        assert len(db['invoices']) == 0
        data_base.set(db)
