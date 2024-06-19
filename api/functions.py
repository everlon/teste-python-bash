import subprocess
import re
# import json

def exec_script_bash(script_path, *args):
    # Função para executar BASH.
    # TODO: Separar em arquivos diferente.

    result = subprocess.run([script_path, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao executar o script Bash: {result.stderr}")
    return result.stdout

def convert_to_json_format(bash_output):
    linhas = bash_output.strip().split('\n')
    users = []
    for linha in linhas:
        match = re.match(r'(\S+@\S+) (\S+) (\d+) size (\d+)', linha)
        if match:
            user = {
                "username": match.group(1),
                "folder": match.group(2),
                "numberMessages": int(match.group(3)),
                "size": int(match.group(4))
            }
            users.append(user)

    return users
    # return json.dumps(users, indent=2)

def filter_users(users, filter_term):
    if filter_term:
        users = [user for user in users if filter_term.lower() in user['username'].lower()]
    return users

def paginate_users(users, page, limit):
    # Paginação: Limit para limitar quantidade por página e Page como número de página

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
