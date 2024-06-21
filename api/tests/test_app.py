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
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_exec_script_order_username(client):
    # Testando se retorna lista de usuários
    response = client.get('/users?file=input&order=asc&page=1&limit=10&filter=fa')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_order_username_no_filename(client):
    # Testando se retorna erro se usuário não informar o nome do arquivo de consulta.
    response = client.get('/users')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo informado não existe.'


def test_exec_script_size_user(client):
    # Testando se retorna lista de usuários com maior ou menor "size".
    response = client.get('/users-size?file=input&size=max')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_size_user_size_incorrect(client):
    # Testando se retorna o usuário com "size" min mesmo se informar errado ou não informar o "size".
    response = client.get('/users-size?file=input&size=bananinha')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_size_user_no_filename(client):
    # Testando se retorna erro se usuário não informar o nome do arquivo de consulta.
    response = client.get('/users-size')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo informado não existe.'


def test_exec_script_users_between_msgs(client):
    # Testando se retorna lista de usuários com limite entre maximo e minimo para "inbox"
    # /users-between-msgs?file=input&min=50&max=200&page=1&filter=example
    response = client.get('/users-between-msgs?file=input&min=50&max=200')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_exec_script_users_between_msgs_no_limit_informed(client):
    # Testando se retorna lista de usuários sem informar limite entre maximo e minimo para "inbox"
    response = client.get('/users-between-msgs?file=input')
    assert response.status_code ==400
    json_data = response.get_json()
    assert json_data['Error'] == 'Informar valor mínimo (min=) e máximo (max=) para faixa de quantidade de mensagens.'

def test_exec_script_users_between_msgs_no_filename(client):
    # Testando se retorna erro se usuário não informar o nome do arquivo de consulta.
    response = client.get('/users-between-msgs')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo informado não existe.'


def test_exec_script_get_files(client):
    # Testando se retorna a lista de arquivos.
    response = client.get('/files?page=1&limit=10')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_file_not_found(client):
    # Testando se retorna arquivo não encontrado pela busca.
    response = client.get('/files?search=nonexistent.txt')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['Error'] == 'Arquivo(s) não encontrado(s).'


def test_file_upload(client):
    # Testando upload de arquivo.
    filepath = os.path.join(os.getcwd(), 'tests', 'testfile.txt')
    with open(filepath, 'w') as f:
        f.write('Arquivo de exemplo para teste.')

    with open(filepath, 'rb') as f:
        data = { 'file': (f, 'testfile.txt') }
        response = client.post('/upload-file', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['msg'] == 'Arquivo salvo com sucesso!'

def test_file_upload_with_existent_file(client):
    # Testando se retorna 204 como arquivo salvo/sobreescrito.
    filepath = os.path.join(os.getcwd(), 'tests', 'testfile.txt')
    filepath_updated = os.path.join(os.getcwd(), '../data/raw', 'testfile.txt')
    with open(filepath, 'rb') as f:
        data = { 'file': (f, 'testfile.txt') }
        response = client.post('/upload-file', data=data, content_type='multipart/form-data')
        assert response.status_code == 204
        # Remove o arquivo após o teste.
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(filepath_updated):
            os.remove(filepath_updated)
