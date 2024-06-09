import time  # Importa o módulo time para medir o tempo de execução
import asyncio  # Importa o módulo asyncio para lidar com programação assíncrona
import os  # Importa o módulo os para operações relacionadas ao sistema operacional
from src.asynchronous import async_main  # Importa a função async_main do módulo src.asynchronous


def benchmark_async(input_file, output_file, buffer_size):
    # Obtém o tamanho total do arquivo de entrada
    total_size = os.path.getsize(input_file)

    # Registra o tempo de início
    start_time = time.time()
    
    # Executa a função assíncrona async_main
    asyncio.run(
        async_main(input_file, output_file, buffer_size, lambda x, y: None, total_size)
    )
    
    # Calcula o tempo de execução da operação assíncrona
    async_time = time.time() - start_time
    
    # Retorna o tempo de execução
    return async_time
