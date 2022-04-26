import pytest
from test.fixtures import clear_fixture, add_file_good, add_file_bad, dummy_data
from src.invoice_search import invoice_search_id, invoice_search_name, get_invoice_data
from src.error import InputError


# testing file for invoice search function

# function test
def test_invoice_search_id(clear_fixture, add_file_good, dummy_data):
    comm_report = add_file_good
    invoice_id = comm_report['invoice_id']
    found_report = invoice_search_id(invoice_id, dummy_data['u_id'])
    assert found_report == comm_report


# search good file by name
def test_invoice_search_name(clear_fixture, add_file_good, dummy_data):
    comm_report = []
    comm_report.append(add_file_good)
    invoice_name = comm_report[0]['invoice_name']
    found_report = invoice_search_name(invoice_name, dummy_data['u_id'])
    assert found_report == comm_report

# searching bad file by name should return communication report of the error


def test_invoice_search_name_bad(clear_fixture, add_file_bad, dummy_data):
    found_report = invoice_search_name('example2.xml', dummy_data['u_id'])
    assert found_report[0]['invoice_name'] == 'example2.xml'


def test_get_invoice_data(clear_fixture, add_file_good, dummy_data):
    invoice_file = open('test/example1.xml', 'r')
    invoice_string = invoice_file.read()
    comm_report = add_file_good

    invoice_id = comm_report['invoice_id']
    content = get_invoice_data(invoice_id, dummy_data['u_id'])
    assert content == invoice_string
