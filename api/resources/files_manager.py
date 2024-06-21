import re
import os

# Permite caracteres alfanuméricos, hífens e underlines
# Usei REGEX para simplificar
ALLOWED_EXTENSIONS = re.compile(r'^[\w\-.]+$')


class FilesManager:
    def __init__(self, data_dir='data/raw'):
        self.data_dir = data_dir


    def search_file(self, search=None):
        # Procurar arquivo na pasta "data/raw". Se não informar search irá listar todos.
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


    def allowed_file(self, filename):
        return ALLOWED_EXTENSIONS.match(filename) is not None
