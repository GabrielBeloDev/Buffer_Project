def synchronous_read_write(input_file, output_file, buffer_size, update_progress, total_size):
    data_list = []

    # Primeira fase: leitura
    with open(input_file, 'r') as infile:
        read_size = 0
        while True:
            data = infile.read(buffer_size)
            if not data:
                break
            print(f"[Síncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            data_list.append(data)
            read_size += len(data)
            update_progress(read_size, total_size)

    # Segunda fase: escrita
    with open(output_file, 'w') as outfile:
        for data in data_list:
            print(f"[Síncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)
