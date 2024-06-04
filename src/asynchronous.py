import asyncio

async def async_read(input_file, buffer_size, update_progress, total_size):
    read_size = 0
    data_list = []
    with open(input_file, 'r') as infile:
        while True:
            data = infile.read(buffer_size)
            if not data:
                break
            print(f"[Assíncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            data_list.append(data)
            read_size += len(data)
            update_progress(read_size, total_size)
    return data_list

async def async_write(output_file, data_list):
    with open(output_file, 'w') as outfile:
        for data in data_list:
            print(f"[Assíncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)

async def async_main(input_file, output_file, buffer_size, update_progress, total_size):
    data_list = await async_read(input_file, buffer_size, update_progress, total_size)
    await async_write(output_file, data_list)
