import time  # Importa o módulo time para medir o tempo de execução
import os  # Importa o módulo os para operações relacionadas ao sistema operacional
from src.synchronous import synchronous_read_write  # Importa a função synchronous_read_write do módulo src.synchronous


def benchmark_sync(input_file, output_file, buffer_size):
    # Obtém o tamanho total do arquivo de entrada
    total_size = os.path.getsize(input_file)

    # Registra o tempo de início
    start_time = time.time()
    
    # Executa a função síncrona synchronous_read_write
    synchronous_read_write(
        input_file, output_file, buffer_size, lambda x, y: None, total_size
    )
    
    # Calcula o tempo de execução da operação síncrona
    sync_time = time.time() - start_time
    
    # Retorna o tempo de execução
    return sync_time
