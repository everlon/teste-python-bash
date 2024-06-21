import os
import json
from re import L
import pytest
from flask import Flask

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'tests', 'uploads')
    app.config['JWT_SECRET_KEY'] = '07OadLS35KQ6V_nO4pQwxzoMy96P5lBr3eWcxYWhpE4'
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def access_token(client):
    response = client.post('/login', json={'username': 'teste', 'password': '123456'})
    return response.get_json()['access_token']



def test_exec_script_order_username(client, access_token):
    # Testando se retorna lista de usuários
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users?file=input&order=asc&page=1&limit=10&filter=fa', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_order_username_no_filename(client, access_token):
    # Testando se retorna erro se usuário não informar o nome do arquivo de consulta.
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users', headers=headers)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo informado não existe.'


def test_exec_script_size_user(client, access_token):
    # Testando se retorna lista de usuários com maior ou menor "size".
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users-size?file=input&size=max', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_size_user_size_incorrect(client, access_token):
    # Testando se retorna o usuário com "size" min mesmo se informar errado ou não informar o "size".
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users-size?file=input&size=bananinha', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_size_user_no_filename(client, access_token):
    # Testando se retorna erro se usuário não informar o nome do arquivo de consulta.
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users-size', headers=headers)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo informado não existe.'


def test_exec_script_users_between_msgs(client, access_token):
    # Testando se retorna lista de usuários com limite entre maximo e minimo para "inbox"
    # /users-between-msgs?file=input&min=50&max=200&page=1&filter=example
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users-between-msgs?file=input&min=50&max=200', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_users_between_msgs_no_limit_informed(client, access_token):
    # Testando se retorna lista de usuários sem informar limite entre maximo e minimo para "inbox"
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users-between-msgs?file=input', headers=headers)
    assert response.status_code ==400
    json_data = response.get_json()
    assert json_data['Error'] == 'Informar valor mínimo (min=) e máximo (max=) para faixa de quantidade de mensagens.'

def test_exec_script_users_between_msgs_no_filename(client, access_token):
    # Testando se retorna erro se usuário não informar o nome do arquivo de consulta.
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/users-between-msgs', headers=headers)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo informado não existe.'


def test_exec_script_get_files(client, access_token):
    # Testando se retorna a lista de arquivos.
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/files?page=1&limit=10', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_file_not_found(client, access_token):
    # Testando se retorna arquivo não encontrado pela busca.
    headers = { 'Authorization': f'Bearer {access_token}' }
    response = client.get('/files?search=nonexistent.txt', headers=headers)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo(s) não encontrado(s).'


def test_file_upload(client, access_token):
    # Testando upload de arquivo.
    headers = { 'Authorization': f'Bearer {access_token}' }
    filepath = os.path.join(os.getcwd(), 'api/tests', 'testfile.txt')

    with open(filepath, 'w') as f:
        f.write('Arquivo de exemplo para teste.')

    with open(filepath, 'rb') as f:
        data = { 'file': (f, 'testfile.txt') }
        response = client.post('/upload-file', data=data, content_type='multipart/form-data', headers=headers)
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['msg'] == 'Arquivo salvo com sucesso!'

def test_file_upload_with_existent_file(client, access_token):
    # Testando se retorna 204 como arquivo salvo/sobreescrito.
    headers = { 'Authorization': f'Bearer {access_token}' }
    filepath = os.path.join(os.getcwd(), 'api/tests', 'testfile.txt')
    filepath_updated = os.path.join(os.getcwd(), 'data/raw', 'testfile.txt')

    with open(filepath, 'rb') as f:
        data = { 'file': (f, 'testfile.txt') }
        response = client.post('/upload-file', data=data, content_type='multipart/form-data', headers=headers)
        assert response.status_code == 204
        # Remove o arquivo após o teste.
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(filepath_updated):
            os.remove(filepath_updated)
