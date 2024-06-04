import time
import os
import logging
from src.synchronous import synchronous_read_write
from src.asynchronous import async_main
import asyncio

# Configura o logger para gravar em arquivo
logger = logging.getLogger("file_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("buffer_project.log")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Configura o logger para imprimir no console
console_logger = logging.getLogger("console_logger")
console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)
console_logger.addHandler(console_handler)


def benchmark(input_file, output_file_sync, output_file_async):
    buffer_size = 1024
    total_size = os.path.getsize(input_file)

    start_time = time.time()
    synchronous_read_write(
        input_file, output_file_sync, buffer_size, lambda x, y: None, total_size
    )
    sync_time = time.time() - start_time
    message_sync = f"Tempo de execução síncrona: {sync_time:.2f} segundos"
    console_logger.info(message_sync)  # Apenas no console
    logger.info(message_sync)

    start_time = time.time()
    asyncio.run(
        async_main(
            input_file, output_file_async, buffer_size, lambda x, y: None, total_size
        )
    )
    async_time = time.time() - start_time
    message_async = f"Tempo de execução assíncrona: {async_time:.2f} segundos"
    console_logger.info(message_async)  # Apenas no console
    logger.info(message_async)


if __name__ == "__main__":
    benchmark("new_input.txt", "output_sync.txt", "output_async.txt")
