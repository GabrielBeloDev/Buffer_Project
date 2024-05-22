import asyncio
from .buffer import AsyncBuffer

async def async_read(input_file, buffer):
    with open(input_file, 'r') as infile: # abre o arquivo de entrada para leitura
        while True:
            data = infile.read(buffer.size) # lê um bloco de dados do tamanho do buffer
            if not data:
                break
            print(f"[Assíncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            await buffer.write_to_buffer(data)

async def async_write(output_file, buffer):
    # Abrir o arquivo de saída para escrita
    with open(output_file, 'w') as outfile:
        while True:
            # Ler dados do buffer e escrever no arquivo de saída
            data = await buffer.read_from_buffer()
            if data is None:
                break
            # Print em português para depuração
            print(f"[Assíncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)

async def async_main(input_file, output_file, buffer_size):
    buffer = AsyncBuffer(buffer_size)
    read_task = asyncio.create_task(async_read(input_file, buffer))
    write_task = asyncio.create_task(async_write(output_file, buffer))
    await read_task
    await write_task
