from .buffer import Buffer

def synchronous_read_write(input_file, output_file, buffer_size):
    buffer = Buffer(buffer_size)
    
    # Abrir o arquivo de entrada para leitura
    with open(input_file, 'r') as infile:
        while True:
            # Ler um bloco de dados do tamanho do buffer
            data = infile.read(buffer_size)
            if not data:
                break
            # Print em português para depuração
            print(f"[Síncrono] Lido do arquivo de entrada: {data.replace('\n', '\\n')}")
            buffer.write_to_buffer(data)
    
    # Abrir o arquivo de saída para escrita
    with open(output_file, 'w') as outfile:
        while True:
            # Ler dados do buffer e escrever no arquivo de saída
            data = buffer.read_from_buffer()
            if data is None:
                break
            # Print em português para depuração
            print(f"[Síncrono] Escrito no arquivo de saída: {data.replace('\n', '\\n')}")
            outfile.write(data)
