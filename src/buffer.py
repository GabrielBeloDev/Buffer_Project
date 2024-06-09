import asyncio  # Importa o módulo asyncio para lidar com programação assíncrona
import logging  # Importa o módulo logging para registrar logs

# Configura o logger para registrar logs em um arquivo chamado "buffer_project.log" no nível INFO
logging.basicConfig(filename="buffer_project.log", level=logging.INFO)

# Função para registrar uma mensagem de log
def log_message(message):
    logging.info(message)


# Classe para implementar um buffer circular síncrono
class CircularBufferSync:
    def __init__(self, size):
        self.size = size  # Define o tamanho do buffer
        self.buffer = [None] * size  # Cria uma lista para armazenar os dados do buffer
        self.start = 0  # Índice de início do buffer
        self.end = 0  # Índice de fim do buffer
        self.full = False  # Indica se o buffer está cheio

    # Método para escrever dados no buffer
    def write_to_buffer(self, data):
        if self.full:
            raise BufferError("Buffer está cheio")  # Levanta um erro se o buffer estiver cheio
        self.buffer[self.end] = data  # Escreve os dados no índice de fim do buffer
        self.end = (self.end + 1) % self.size  # Atualiza o índice de fim de forma circular
        if self.end == self.start:
            self.full = True  # Marca o buffer como cheio se os índices de início e fim coincidirem

    # Método para ler dados do buffer
    def read_from_buffer(self):
        if self.start == self.end and not self.full:
            return None  # Retorna None se o buffer estiver vazio
        data = self.buffer[self.start]  # Lê os dados do índice de início do buffer
        self.buffer[self.start] = None  # Limpa a posição lida
        self.start = (self.start + 1) % self.size  # Atualiza o índice de início de forma circular
        self.full = False  # Marca o buffer como não cheio após a leitura
        return data


# Classe para implementar um buffer circular assíncrono
class CircularBufferAsync:
    def __init__(self, size):
        self.size = size  # Define o tamanho do buffer
        self.buffer = [None] * size  # Cria uma lista para armazenar os dados do buffer
        self.start = 0  # Índice de início do buffer
        self.end = 0  # Índice de fim do buffer
        self.full = False  # Indica se o buffer está cheio
        self.lock = asyncio.Lock()  # Cria um lock para garantir a exclusão mútua nas operações assíncronas

    # Método assíncrono para escrever dados no buffer
    async def write_to_buffer(self, data):
        async with self.lock:
            if self.full:
                raise BufferError("Buffer está cheio")  # Levanta um erro se o buffer estiver cheio
            self.buffer[self.end] = data  # Escreve os dados no índice de fim do buffer
            self.end = (self.end + 1) % self.size  # Atualiza o índice de fim de forma circular
            if self.end == self.start:
                self.full = True  # Marca o buffer como cheio se os índices de início e fim coincidirem

    # Método assíncrono para ler dados do buffer
    async def read_from_buffer(self):
        async with self.lock:
            if self.start == self.end and not self.full:
                return None  # Retorna None se o buffer estiver vazio
            data = self.buffer[self.start]  # Lê os dados do índice de início do buffer
            self.buffer[self.start] = None  # Limpa a posição lida
            self.start = (self.start + 1) % self.size  # Atualiza o índice de início de forma circular
            self.full = False  # Marca o buffer como não cheio após a leitura
            return data
