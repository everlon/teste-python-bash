import subprocess
import re
import os
# import json


class BashManager:
    def __init__(self, data_dir='../data/raw'):
        self.data_dir = data_dir

    def exec_script_bash(self, script_path, *args):
        # Função para executar BASH.

        result = subprocess.run([f"./../scripts/bash/{script_path}", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"Erro ao executar o script Bash: {result.stderr}")
        return result.stdout

    def convert_to_json_format(self, bash_output):
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

    def filter_users(self, users, filter_term):
        if filter_term:
            users = [user for user in users if filter_term.lower() in user['username'].lower()]
        return users

    def search_file(self, search=None):
        # Procurar arquivo na pasta "../data/raw". Se não informar search irá listar todos.
        try:
            files = os.listdir(self.data_dir)

            if search:
                # Selecionar o arquivo de nome idêntico ao informado.
                return [f for f in files if f == search and os.path.isfile(os.path.join(self.data_dir, f))]
            else:
                # Retorna todos os arquivos da pasta '../data/raw'.
                return [f for f in files if os.path.isfile(os.path.join(self.data_dir, f))]

        except FileNotFoundError:
            return []

    def paginate_users(self, users, page, limit):
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
