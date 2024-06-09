import logging  # Importa o módulo logging para registrar logs

# Configura o logger para registrar logs em um arquivo chamado "buffer_project.log" no nível INFO
logging.basicConfig(filename="buffer_project.log", level=logging.INFO)

# Função para registrar uma mensagem de log
def log_message(message):
    logging.info(message)
