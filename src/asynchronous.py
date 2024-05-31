import asyncio
from .buffer import AsyncBuffer
import os

async def async_read(input_file, buffer, update_progress, total_size):
    read_size = 0

    with open(input_file, 'r') as infile:
        while True:
            data = infile.read(buffer.size)
            if not data:
                break
            print(f"[Assíncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            await buffer.write_to_buffer(data)
            read_size += len(data)
            update_progress(read_size, total_size)

async def async_write(output_file, buffer):
    with open(output_file, 'w') as outfile:
        while True:
            data = await buffer.read_from_buffer()
            if data is None:
                break
            print(f"[Assíncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)

async def async_main(input_file, output_file, buffer_size, update_progress, total_size):
    buffer = AsyncBuffer(buffer_size)
    read_task = asyncio.create_task(async_read(input_file, buffer, update_progress, total_size))
    write_task = asyncio.create_task(async_write(output_file, buffer))
    await read_task
    await write_task