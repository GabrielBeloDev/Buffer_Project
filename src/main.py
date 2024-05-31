import sys  # Importa o módulo sys para manipulação do caminho do sistema
import os  # Importa o módulo os para interações com o sistema operacional

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.path.abspath(__file__) retorna o caminho absoluto do arquivo atual
# os.path.dirname() obtém o diretório pai do caminho fornecido
# A segunda chamada os.path.dirname() obtém o diretório pai do diretório anterior
# sys.path.append() adiciona esse diretório ao caminho do sistema para que os módulos possam ser importados

from ui.app import start_app  # Importa a função start_app do módulo ui.app

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    start_app()  # Inicia a aplicação chamando a função start_app
