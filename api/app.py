import re
import os
from flask import Flask, request, jsonify
from markupsafe import escape

from resources.users_manager import UsersManager
from resources.bash_manager import BashManager
from resources.files_manager import FilesManager


def create_app():
    app = Flask(__name__)

    # Usando os recursos da API
    users_manager = UsersManager()
    bash_manager = BashManager()
    files_manager = FilesManager()

    # Certifique-se de que a pasta de upload existe
    UPLOAD_FOLDER = 'data/raw'
    os.makedirs((UPLOAD_FOLDER), exist_ok=True)



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
        try:
            if 'file' not in request.files:
                app.logger.error('Nenhum arquivo informado pelo usuário.')
                return jsonify({"Error": "Nenhum arquivo informado pelo usuário."}), 201

            file = request.files['file']

            if file and files_manager.allowed_file(file.filename):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)

                file_check = files_manager.search_file(file.filename)
                if not file_check:
                    file.save(filepath)
                    app.logger.info('Arquivo salvo com sucesso!')
                    return jsonify({"msg": "Arquivo salvo com sucesso!"}), 200
                else:
                    file.save(filepath)
                    app.logger.info('Arquivo substituído com sucesso!')
                    return jsonify({"msg": "Arquivo substituído com sucesso!"}), 204

            else:
                app.logger.error('Nome do arquivo não é suportado.')
                return jsonify({"Error": "Nome do arquivo não suportado. Certifique-se que não tenha caracteres especiais no nome do arquivo."}), 400

        except Exception as e:
                app.logger.error('Ocorreu um erro: (%s)', e)
                return f"Error: {e}", 500


    # ROUTE 2: Listar arquivos armazenados.
    # /files?page=1&limit=10&search=file.txt
    @app.route('/files', methods=['GET'])
    def exec_script_get_files():
        try:
            search = request.args.get('search', default='', type=str)
            page = request.args.get('page', default=1, type=int)
            limit = request.args.get('limit', default=10, type=int)

            files = files_manager.search_file(search)

            if not files:
                app.logger.error('Arquivo(s) não encontrado(s).')
                return jsonify({"Error": "Arquivo(s) não encontrado(s)."}), 404

            files = users_manager.paginate_users(files, page, limit)

            app.logger.info('Arquivos encontrados com sucesso!')
            return jsonify(files), 200

        except Exception as e:
            app.logger.error('Ocorreu um erro: (%s)', e)
            return f"Error: {e}", 500


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

            file = files_manager.search_file(arquivo)

            if not arquivo or not file:
                app.logger.error('Arquivo informado não existe.')
                return jsonify({"Error": "Arquivo informado não existe."}), 404

            bash_output = bash_manager.exec_script_bash('max-min-size.sh', f"{UPLOAD_FOLDER}/{file[0]}", size)
            app.logger.info('Script BASH (order-by-username.sh) executado com sucesso!')

            users = users_manager.convert_to_json_format(bash_output)

            return jsonify(users), 200

        except Exception as e:
            app.logger.error('Ocorreu um erro: (%s)', e)
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

            file = files_manager.search_file(arquivo)

            if not arquivo or not file:
                app.logger.error('Arquivo informado não existe.')
                return jsonify({"Error": "Arquivo informado não existe."}), 404

            bash_output = bash_manager.exec_script_bash('order-by-username.sh', f"{UPLOAD_FOLDER}/{file[0]}", order)
            app.logger.info('Script BASH (order-by-username.sh) executado com sucesso!')

            users = users_manager.convert_to_json_format(bash_output)
            users = users_manager.filter_users(users, filter_term)
            users = users_manager.paginate_users(users, page, limit)

            return jsonify(users), 200

        except Exception as e:
            app.logger.error('Ocorreu um erro: (%s)', e)
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

            file = files_manager.search_file(arquivo)

            if not arquivo or not file:
                app.logger.error('Arquivo informado não existe.')
                return jsonify({"Error": "Arquivo informado não existe."}), 404

            if not limit_min and not limit_max:
                return {"Error": "Informar valor mínimo (min=) e máximo (max=) para faixa de quantidade de mensagens."}, 400

            page = request.args.get('page', default=1, type=int)
            limit = request.args.get('limit', default=0)
            filter_term = request.args.get('filter', default='')

            bash_output = bash_manager.exec_script_bash('between-msgs.sh', f"{UPLOAD_FOLDER}/{file[0]}", limit_min, limit_max)
            app.logger.info('Script BASH (between-msgs.sh) executado com sucesso!')

            users = users_manager.convert_to_json_format(bash_output)
            users = users_manager.filter_users(users, filter_term)
            users = users_manager.paginate_users(users, page, limit)

            return jsonify(users), 200

        except Exception as e:
            app.logger.error('Ocorreu um erro: (%s)', e)
            return f"Error: {e}", 500



    # Exemplo de retorno com número de Erros em JSON.
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error('Rota não encontrada: 404')
        return {"msg": 'ERRO 404!'}, 404


    # Retorno de teste_PeoplePro_app()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()


# Rodar aplicação flask.
# flask --app api/app run --debug
