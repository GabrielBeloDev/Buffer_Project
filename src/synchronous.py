from .buffer import Buffer
import os

def synchronous_read_write(input_file, output_file, buffer_size, update_progress, total_size):
    buffer = Buffer(buffer_size)
    read_size = 0

    with open(input_file, 'r') as infile:
        while True:
            data = infile.read(buffer_size)
            if not data:
                break
            print(f"[Síncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            buffer.write_to_buffer(data)
            read_size += len(data)
            update_progress(read_size, total_size)

    with open(output_file, 'w') as outfile:
        while True:
            data = buffer.read_from_buffer()
            if data is None:
                break
            print(f"[Síncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)