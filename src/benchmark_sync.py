import time
import os
from src.synchronous import synchronous_read_write


def benchmark_sync(input_file, output_file, buffer_size):
    total_size = os.path.getsize(input_file)

    start_time = time.time()
    synchronous_read_write(
        input_file, output_file, buffer_size, lambda x, y: None, total_size
    )
    sync_time = time.time() - start_time
    return sync_time
