from flask import Flask, request, jsonify

app = Flask(__name__)


def paginate_users(users, page, limit):
    page = int(page)
    limit = int(limit)

    if limit <= 0:
        return users

    start = (page - 1) * limit
    end = start + limit

    if start >= len(users):
        return []

    if end > len(users):
        end = len(users)

    return users[start:end]


@app.route('/', methods=['GET', 'POST'])
def index():
    users = [
        {"username": "user1", "email": "user1@example.com"},
        {"username": "user2", "email": "user2@example.com"},
        {"username": "user3", "email": "user3@example.com"},
        {"username": "user4", "email": "user4@example.com"},
        {"username": "user5", "email": "user5@example.com"},
        {"username": "user6", "email": "user6@example.com"},
        {"username": "user7", "email": "user7@example.com"},
        {"username": "user8", "email": "user8@example.com"},
        {"username": "user9", "email": "user9@example.com"},
        {"username": "user10", "email": "user10@example.com"},
        {"username": "user11", "email": "user11@example.com"},
        {"username": "user12", "email": "user12@example.com"},
        {"username": "user13", "email": "user13@example.com"},
        {"username": "user14", "email": "user14@example.com"},
        {"username": "user15", "email": "user15@example.com"},
        {"username": "user16", "email": "user16@example.com"},
        {"username": "user17", "email": "user17@example.com"},
        {"username": "user18", "email": "user18@example.com"},
        {"username": "user19", "email": "user19@example.com"},
        {"username": "user20", "email": "user20@example.com"},
        {"username": "user21", "email": "user21@example.com"},
        {"username": "user22", "email": "user22@example.com"},
        {"username": "user23", "email": "user23@example.com"},
        {"username": "user24", "email": "user24@example.com"},
        {"username": "user25", "email": "user25@example.com"},
        {"username": "user26", "email": "user26@example.com"},
        {"username": "user27", "email": "user27@example.com"},
        {"username": "user28", "email": "user28@example.com"},
        {"username": "user29", "email": "user29@example.com"},
        {"username": "user30", "email": "user30@example.com"},
        {"username": "user31", "email": "user31@example.com"},
        {"username": "user32", "email": "user32@example.com"},
        {"username": "user33", "email": "user33@example.com"},
        {"username": "user34", "email": "user34@example.com"},
        {"username": "user35", "email": "user35@example.com"},
        {"username": "user36", "email": "user36@example.com"},
        {"username": "user37", "email": "user37@example.com"},
        {"username": "user38", "email": "user38@example.com"},
        {"username": "user39", "email": "user39@example.com"},
        {"username": "user40", "email": "user40@example.com"},
        {"username": "user41", "email": "user41@example.com"},
        {"username": "user42", "email": "user42@example.com"},
        {"username": "user43", "email": "user43@example.com"},
        {"username": "user44", "email": "user44@example.com"},
        {"username": "user45", "email": "user45@example.com"},
        {"username": "user46", "email": "user46@example.com"},
        {"username": "user47", "email": "user47@example.com"},
        {"username": "user48", "email": "user48@example.com"},
        {"username": "user49", "email": "user49@example.com"},
        {"username": "user50", "email": "user50@example.com"}
    ]

    # Parâmetros para paginação
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    # Chamada da função de paginação
    paginated_users = paginate_users(users, page, limit)

    # Exemplo de como você pode retornar os usuários paginados
    return jsonify(paginated_users), 200
