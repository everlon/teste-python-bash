from flask import Flask, request, jsonify
from markupsafe import escape

from functions import BashManager


app = Flask(__name__)
bash_manager = BashManager()

# Exemplo de Methods e já retorna Json por default.
@app.route('/', methods=['GET', 'POST'])
def index():
    user = {
        "username": 'everlon',
        "theme": 'classic',
        "image": 'perfil.png',
    }
    return user, 200


# Exemplo de Parâmetro na URL e Loggings.
@app.route('/user/<username>')
def show_user_profile(username):
    # app.logger.debug('A value for debugging')
    # app.logger.info('Doing something')
    # app.logger.warning('A warning occurred (%d apples)', 42)
    # app.logger.error('An error occurred')
    # app.logger.critical('An error critical occurred')

    app.logger.warning('Informando usuário (%s) por URL.', escape(username))
    return f'User {escape(username)}', 200


# ROUTE 4: Usuários.
# /users?file=input&order=asc&page=1&limit=15&filter=example
@app.route('/users', methods=['GET'])
def exec_script_order_username():
    try:
        arquivo = request.args.get('file', default='', type=str)
        file = bash_manager.search_file(arquivo)

        if not arquivo or not file:
            return {"Error": "Arquivo informado não existe."}, 404

        order = request.args.get('order', default='asc', type=str)
        limit = request.args.get('limit', default=0)
        page = request.args.get('page', default=1, type=int)
        filter_term = request.args.get('filter', default='')

        bash_output = bash_manager.exec_script_bash('./../scripts/bash/order-by-username.sh', f"../data/raw/{file[0]}", order)
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
@app.route('/users-between', methods=['GET'])
def executar_script():
    try:
        arquivo = request.args.get('file', default='', type=str)
        file = bash_manager.search_file(arquivo)

        if not arquivo or not file:
            return {"Error": "Arquivo informado não existe."}, 404

        limit_min = request.args.get('min')
        limit_max = request.args.get('max')

        if not limit_min and not limit_max:
            return {"Error": "Informar valor mínimo (min=) e máximo (max=) para faixa de quantidade de mensagens."}, 400

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=0)
        filter_term = request.args.get('filter', default='')

        bash_output = bash_manager.exec_script_bash('./../scripts/bash/between-msgs.sh', f"../data/raw/{file[0]}", limit_min, limit_max)
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
