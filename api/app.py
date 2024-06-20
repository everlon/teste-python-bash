import re, os
from flask import Flask, request, jsonify
from markupsafe import escape

from functions import BashManager


app = Flask(__name__)
bash_manager = BashManager()

# Certifique-se de que a pasta de upload existe
UPLOAD_FOLDER = '../data/raw'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# ROUTE HOME: Mensagem de boas-vindas.
@app.route('/', methods=['GET', 'POST'])
def index():
    # app.logger.debug('A value for debugging')
    # app.logger.warning('A warning occurred (%d apples)', 42)
    # app.logger.error('An error occurred')
    # app.logger.critical('An error critical occurred')

    app.logger.info('Mensagens de boas vindas.')
    return { "msg": 'Bem vindo(a)!' }, 200


# ROUTE 1: Upload de arquivo.
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('Nenhum arquivo informado pelo usuário.')
        return jsonify({"Error": "Nenhum arquivo informado pelo usuário."}), 400

    file = request.files['file']

    if file and bash_manager.allowed_file(file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        app.logger.info('Arquivo salvo com sucesso!')
        return jsonify({"msg": "Arquivo salvo com sucesso!"}), 200
    else:
        app.logger.error('Nome do arquivo não é suportado.')
        return jsonify({"Error": "Nome do arquivo não suportado. Certifique-se que não tenha caracteres especiais no nome do arquivo."}), 400


# ROUTE 2: Listar arquivos armazenados.
# /files?page=1&limit=10
@app.route('/files', methods=['GET'])
def exec_script_get_files():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    files = bash_manager.search_file()
    print(files)

    if not files:
        app.logger.error('Arquivos não encontrados.')
        return jsonify({"Error": "Nenhum arquivo armazenado."}), 404

    files = bash_manager.paginate_users(files, page, limit)

    app.logger.info('Arquivos encontrados com sucesso!')
    return jsonify(files), 200


# ROUTE 3: Usuários com maior size.
# /users?file=input&size=max
@app.route('/users-size', methods=['GET'])
def exec_script_size_user():
    try:
        if request.is_json:
            # Verifica se enviou por Raw/JSON
            data = request.get_json()
            arquivo = data.get('file', None)
            size = data.get('size', None)
        else:
            # Enviado por Parâmetros URL
            arquivo = request.args.get('file', default='', type=str)
            size = request.args.get('size', default='', type=str)

        size = 'min' if size == 'min' else '' # Defina "min" caso tenha colocado valor no parâmetro site da URL.

        file = bash_manager.search_file(arquivo)

        if not arquivo or not file:
            app.logger.error('Arquivo informado não existe.')
            return jsonify({"Error": "Arquivo informado não existe."}), 404

        bash_output = bash_manager.exec_script_bash('max-min-size.sh', f"../data/raw/{file[0]}", size)
        app.logger.info('Script BASH (order-by-username.sh) executado com sucesso!')

        users = bash_manager.convert_to_json_format(bash_output)

        return jsonify(users), 200

    except Exception as e:
        app.logger.error('An error occurred: (%s)', e)
        return f"Error: {e}", 500


# ROUTE 4: Usuários.
# /users?file=input&order=asc&page=1&limit=15&filter=example
@app.route('/users', methods=['GET'])
def exec_script_order_username():
    try:
        if request.is_json:
            # Verifica se enviou por Raw/JSON
            data = request.get_json()
            arquivo = data.get('file', '')
            order = data.get('order', 'asc')
            limit = data.get('limit', 0)
            page = data.get('page', 1)
            filter_term = data.get('filter', '')
        else:
            # Enviado por Parâmetros URL
            arquivo = request.args.get('file', default='', type=str)
            order = request.args.get('order', default='asc', type=str)
            limit = request.args.get('limit', default=0)
            page = request.args.get('page', default=1, type=int)
            filter_term = request.args.get('filter', default='')

        file = bash_manager.search_file(arquivo)

        if not arquivo or not file:
            app.logger.error('Arquivo informado não existe.')
            return jsonify({"Error": "Arquivo informado não existe."}), 404

        bash_output = bash_manager.exec_script_bash('order-by-username.sh', f"../data/raw/{file[0]}", order)
        app.logger.info('Script BASH (order-by-username.sh) executado com sucesso!')

        users = bash_manager.convert_to_json_format(bash_output)
        users = bash_manager.filter_users(users, filter_term)
        users = bash_manager.paginate_users(users, page, limit)

        return jsonify(users), 200

    except Exception as e:
        app.logger.error('An error occurred: (%s)', e)
        return f"Error: {e}", 500


# ROUTE 5: Quantidade de mensagens na INBOX.
# /users-between?file=input&min=50&max=200&page=1&filter=example
@app.route('/users-between-msgs', methods=['GET'])
def exec_script_users_between_msgs():
    try:
        if request.is_json:
            # Verifica se enviou por Raw/JSON
            data = request.get_json()
            arquivo = data.get('file', '')
            limit_min = str(data.get('min')) # Campo obrigatório
            limit_max = str(data.get('max')) # Campo obrigatório
        else:
            # Enviado por Parâmetros URL
            arquivo = request.args.get('file', default='', type=str)
            limit_min = request.args.get('min') # Campo obrigatório
            limit_max = request.args.get('max') # Campo obrigatório

        file = bash_manager.search_file(arquivo)

        if not arquivo or not file:
            app.logger.error('Arquivo informado não existe.')
            return jsonify({"Error": "Arquivo informado não existe."}), 404

        if not limit_min and not limit_max:
            return {"Error": "Informar valor mínimo (min=) e máximo (max=) para faixa de quantidade de mensagens."}, 400

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=0)
        filter_term = request.args.get('filter', default='')

        bash_output = bash_manager.exec_script_bash('between-msgs.sh', f"../data/raw/{file[0]}", limit_min, limit_max)
        app.logger.info('Script BASH (between-msgs.sh) executado com sucesso!')

        users = bash_manager.convert_to_json_format(bash_output)
        users = bash_manager.filter_users(users, filter_term)
        users = bash_manager.paginate_users(users, page, limit)

        return jsonify(users), 200

    except Exception as e:
        app.logger.error('An error occurred: (%s)', e)
        return f"Error: {e}", 500



# Exemplo de retorno com número de Erros em JSON.
@app.errorhandler(404)
def not_found(error):
    app.logger.error('An error occurred: 404')
    return {"msg": 'ERRO 404!'}, 404



if __name__ == '__main__':
    app.run(debug=True)


# Rodar aplicação flask.
# flask --app app run --debug
