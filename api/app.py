from flask import Flask, request, jsonify
from markupsafe import escape

import functions as Func


app = Flask(__name__)


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


# Exemplo de executar BASH.
@app.route('/executar-script', methods=['GET'])
def executar_script():
    try:
        arquivo = "../data/raw/input"
        limite_inferior = "50"
        limite_superior = "200"
        bash_output = Func.exec_script_bash('./../scripts/bash/between-msgs.sh', arquivo, limite_inferior, limite_superior)
        app.logger.info('Script BASH (between-msgs.sh) executado com sucesso!')

        return jsonify(Func.convert_to_json_format(bash_output)), 200

    except Exception as e:
        app.logger.error('An error occurred: (%s)', e)
        return f"Erro: {e}", 500


# ROUTE usuários ordenados.
# /users?order=asc&limit=15&page=1&filter=example
@app.route('/users', methods=['GET'])
def exec_script_order_username():
    try:
        arquivo = "../data/raw/input"
        order = request.args.get('order', default='asc', type=str)
        limit = request.args.get('limit')
        page = request.args.get('page', default=1, type=int)
        filter_term = request.args.get('filter', default='')

        bash_output = Func.exec_script_bash('./../scripts/bash/order-by-username.sh', arquivo, order)
        app.logger.info('Script BASH (order-by-username.sh) executado com sucesso!')

        users = Func.convert_to_json_format(bash_output)
        users = Func.filter_users(users, filter_term)
        users = Func.paginate_users(users, page, limit)

        return jsonify(users), 200

    except Exception as e:
        app.logger.error('An error occurred: (%s)', e)
        return f"Erro: {e}", 500


# Exemplo de retorno com número de Erros em JSON.
@app.errorhandler(404)
def not_found(error):
    app.logger.error('An error occurred: 404')
    return {"msg": 'ERRO 404!'}, 404



if __name__ == '__main__':
    app.run(debug=True)


# Rodar aplicação flask.
# flask --app app run
