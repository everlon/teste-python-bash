import subprocess
import json
import re

'''
    Este arquivo é somente um teste para verificar a execução de
    um BASH pelo Python nos conformes do Teste.
'''

def exec_script_bash(script_path, *args):
    result = subprocess.run([script_path, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao executar o script Bash: {result.stderr}")
    return result.stdout

def convert_to_json(bash_output):
    linhas = bash_output.strip().split('\n')
    usuarios = []
    for linha in linhas:
        match = re.match(r'(\S+@\S+) (\S+) (\d+) size (\d+)', linha)
        if match:
            usuario = {
                "username": match.group(1),
                "folder": match.group(2),
                "numberMessages": int(match.group(3)),
                "size": int(match.group(4))
            }
            usuarios.append(usuario)
    return json.dumps(usuarios, indent=2)


def main():
    try:
        arquivo = "data/raw/input"
        limite_inferior = "50"
        limite_superior = "200"
        bash_output = exec_script_bash('./scripts/bash/between-msgs.sh', arquivo, limite_inferior, limite_superior)
        json_output = convert_to_json(bash_output)

        print(json_output)

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
