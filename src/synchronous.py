def synchronous_read_write(input_file, output_file, buffer_size, update_progress, total_size):
    data_list = []  # Inicializa uma lista para armazenar os dados lidos

    # Primeira fase: leitura
    with open(input_file, 'r') as infile:  # Abre o arquivo de entrada para leitura
        read_size = 0  # Inicializa o contador de tamanho lido
        while True:  # Loop para ler o arquivo em partes
            data = infile.read(buffer_size)  # Lê uma parte do arquivo com o tamanho especificado pelo buffer
            if not data:  # Se não houver mais dados para ler, sai do loop
                break
            print(f"[Síncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")  # Imprime os dados lidos substituindo quebras de linha por '\n'
            data_list.append(data)  # Adiciona os dados lidos à lista
            read_size += len(data)  # Atualiza o tamanho total lido
            update_progress(read_size, total_size)  # Chama a função de atualização de progresso com o tamanho lido e o tamanho total

    # Segunda fase: escrita
    with open(output_file, 'w') as outfile:  # Abre o arquivo de saída para escrita
        for data in data_list:  # Itera sobre os dados armazenados na lista
            print(f"[Síncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")  # Imprime os dados a serem escritos substituindo quebras de linha por '\n'
            outfile.write(data)  # Escreve os dados no arquivo de saída
