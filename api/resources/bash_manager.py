import subprocess


class BashManager:
    def __init__(self, scripts_bash='scripts/bash'):
        self.scripts_bash = scripts_bash

    def exec_script_bash(self, script_path, *args):
        # Função para executar BASH.
        result = subprocess.run([f"./{self.scripts_bash}/{script_path}", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            raise Exception(f"Erro ao executar o script Bash: {result.stderr}")

        return result.stdout
