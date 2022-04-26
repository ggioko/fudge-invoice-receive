from src.config import url
import requests
import json

def test_register_simple():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'good@email.com', 'password': 'hello123'})
    assert json.loads(response.text) == {}
    assert response.status_code == 200

def test_register_multiple_users(): 
     requests.delete(url + 'clear/')
     response1 = requests.post(f'{url}auth_register/', json={'email': 'a@email.com', 'password': 'hello123'})
     response2 = requests.post(f'{url}auth_register/', json={'email': 'b@email.com', 'password': 'hello123'})
     response3 = requests.post(f'{url}auth_register/', json={'email': 'c@email.com', 'password': 'hello123'})
     assert response1.status_code == 200
     assert response2.status_code == 200
     assert response3.status_code == 200

def test_register_duplicate_email():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'good@email.com', 'password': 'hello123'})
    assert json.loads(response.text) == {}
    assert response.status_code == 200

    response = requests.post(f'{url}auth_register/', json={'email': 'good@email.com', 'password': 'hello123'})
    assert response.status_code == 400

# Testing email requirements 
def test_register_bad_email1():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'abc', 'password': 'hello123'})
    assert response.status_code == 400

def test_register_bad_email2():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'abc@gmail', 'password': 'hello123'})
    assert response.status_code == 400

def test_register_bad_email3():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'abc@gmail.c', 'password': 'hello123'})
    assert response.status_code == 400

def test_register_bad_email4():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'abc@.com', 'password': 'hello123'})
    assert response.status_code == 400

def test_register_bad_email5():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': '@gmail.com', 'password': 'hello123'})
    assert response.status_code == 400

# Testing password requirements 
def test_register_bad_password():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'bad@email.com', 'password': 'hell'})
    assert response.status_code == 400

def test_register_empty_password():
    requests.delete(url + 'clear/')
    response = requests.post(f'{url}auth_register/', json={'email': 'bad@email.com', 'password': ''})
    assert response.status_code == 400