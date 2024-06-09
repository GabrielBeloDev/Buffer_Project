import asyncio

# Função assíncrona para ler o conteúdo de um arquivo
async def async_read(input_file, buffer_size, update_progress, total_size):
    read_size = 0  # Variável para manter o controle do tamanho lido até o momento
    data_list = []  # Lista para armazenar os dados lidos
    with open(input_file, 'r') as infile:  # Abre o arquivo de entrada no modo de leitura
        while True:  # Loop para ler o arquivo continuamente até o final
            data = infile.read(buffer_size)  # Lê um pedaço do arquivo com tamanho definido por buffer_size
            if not data:  # Se não houver mais dados para ler, sai do loop
                break
            # Exibe no console o conteúdo lido, substituindo quebras de linha por '\n' para melhor visualização
            print(f"[Assíncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            data_list.append(data)  # Adiciona o pedaço lido à lista de dados
            read_size += len(data)  # Atualiza o tamanho total lido
            update_progress(read_size, total_size)  # Chama a função de atualização de progresso com o tamanho lido e o tamanho total do arquivo
    return data_list  # Retorna a lista de dados lidos

# Função assíncrona para escrever o conteúdo em um arquivo
async def async_write(output_file, data_list):
    with open(output_file, 'w') as outfile:  # Abre o arquivo de saída no modo de escrita
        for data in data_list:  # Itera sobre a lista de dados a serem escritos
            # Exibe no console o conteúdo que será escrito, substituindo quebras de linha por '\n' para melhor visualização
            print(f"[Assíncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)  # Escreve o pedaço de dados no arquivo de saída

# Função principal assíncrona que orquestra a leitura e escrita dos arquivos
async def async_main(input_file, output_file, buffer_size, update_progress, total_size):
    # Chama a função de leitura assíncrona e aguarda sua conclusão
    data_list = await async_read(input_file, buffer_size, update_progress, total_size)
    # Chama a função de escrita assíncrona e aguarda sua conclusão
    await async_write(output_file, data_list)
