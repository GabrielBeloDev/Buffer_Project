import time  # Importa o módulo time para medir o tempo de execução
import os  # Importa o módulo os para operações relacionadas ao sistema operacional
import logging  # Importa o módulo logging para registrar logs
from src.synchronous import synchronous_read_write  # Importa a função synchronous_read_write do módulo src.synchronous
from src.asynchronous import async_main  # Importa a função async_main do módulo src.asynchronous
import asyncio  # Importa o módulo asyncio para lidar com programação assíncrona

# Configura o logger para gravar em arquivo
logger = logging.getLogger("file_logger")  # Cria um logger chamado "file_logger"
logger.setLevel(logging.INFO)  # Define o nível de log para INFO
file_handler = logging.FileHandler("buffer_project.log")  # Cria um manipulador de arquivo para gravar logs em "buffer_project.log"

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # Define o formato dos logs
file_handler.setFormatter(formatter)  # Associa o formato ao manipulador de arquivo

logger.addHandler(file_handler)  # Adiciona o manipulador de arquivo ao logger

# Configura o logger para imprimir no console
console_logger = logging.getLogger("console_logger")  # Cria um logger chamado "console_logger"
console_logger.setLevel(logging.INFO)  # Define o nível de log para INFO
console_handler = logging.StreamHandler()  # Cria um manipulador de fluxo para imprimir logs no console

console_handler.setFormatter(formatter)  # Associa o formato ao manipulador de console
console_logger.addHandler(console_handler)  # Adiciona o manipulador de console ao logger


def benchmark(input_file, output_file_sync, output_file_async):
    buffer_size = 1024  # Define o tamanho do buffer para leitura/escrita
    total_size = os.path.getsize(input_file)  # Obtém o tamanho total do arquivo de entrada

    # Medição do tempo de execução da função síncrona
    start_time = time.time()  # Registra o tempo de início
    synchronous_read_write(
        input_file, output_file_sync, buffer_size, lambda x, y: None, total_size
    )
    sync_time = time.time() - start_time  # Calcula o tempo de execução
    message_sync = f"Tempo de execução síncrona: {sync_time:.2f} segundos"  # Cria uma mensagem de log
    console_logger.info(message_sync)  # Registra a mensagem no console
    logger.info(message_sync)  # Registra a mensagem no arquivo de log

    # Medição do tempo de execução da função assíncrona
    start_time = time.time()  # Registra o tempo de início
    asyncio.run(
        async_main(
            input_file, output_file_async, buffer_size, lambda x, y: None, total_size
        )
    )
    async_time = time.time() - start_time  # Calcula o tempo de execução
    message_async = f"Tempo de execução assíncrona: {async_time:.2f} segundos"  # Cria uma mensagem de log
    console_logger.info(message_async)  # Registra a mensagem no console
    logger.info(message_async)  # Registra a mensagem no arquivo de log


if __name__ == "__main__":
    benchmark("new_input.txt", "output_sync.txt", "output_async.txt")  # Executa a função benchmark com arquivos de entrada e saída especificados
