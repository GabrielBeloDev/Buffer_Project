import time
import asyncio
import os
from src.asynchronous import async_main


def benchmark_async(input_file, output_file, buffer_size):
    total_size = os.path.getsize(input_file)

    start_time = time.time()
    asyncio.run(
        async_main(input_file, output_file, buffer_size, lambda x, y: None, total_size)
    )
    async_time = time.time() - start_time
    return async_time
