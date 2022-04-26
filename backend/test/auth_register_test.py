import pytest
from test.fixtures import clear_fixture
import re
from src.auth import register 
from src.error import InputError


def test_register_simple(clear_fixture):
    register('good@email.com', 'hello123')

# Testing that multiple users can register consecutively 
def test_register_multiple_users(clear_fixture):
    register('a@gmail.com', 'hello123')
    register('b@gmail.com', 'hello123')
    register('c@gmail.com', 'hello123')

# Same email cannot be used twice to register
def test_duplicate_email(clear_fixture):
    register('a@gmail.com', 'hello123')
    with pytest.raises(InputError):
        register('a@gmail.com', 'hello123')

# Testing email requirements
def test_invalid_email1(clear_fixture):
    with pytest.raises(InputError):
        register('abc', 'hello123')

def test_invalid_email2(clear_fixture):
    with pytest.raises(InputError):
        register('abc@gmail', 'hello123')

def test_invalid_email3(clear_fixture):
    with pytest.raises(InputError):
        register('abc@gmail.c', 'hello123')

def test_invalid_email4(clear_fixture):
    with pytest.raises(InputError):
        register('abc@.com', 'hello123')

def test_invalid_email5(clear_fixture):
    with pytest.raises(InputError):
        register('@gmail.com', 'hello123')

# Testing password requirements 
def test_invalid_password(clear_fixture):
    with pytest.raises(InputError):
        register('good@email.com', 'hell')

def test_empty_password(clear_fixture):
    with pytest.raises(InputError):
        register('good@email.com', '')

# Testing both invalid password and email together 
def test_invalid_email_password(clear_fixture):
    with pytest.raises(InputError):
        register('bademail', 'hell')
