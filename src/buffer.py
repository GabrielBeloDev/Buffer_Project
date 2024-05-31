import asyncio  # Importa a biblioteca asyncio para suporte a operações assíncronas


# Define a classe Buffer para operações síncronas
class Buffer:
    def __init__(self, size):
        self.size = size  # Define o tamanho do buffer
        self.buffer = []  # Inicializa a lista que armazena os dados do buffer

    def write_to_buffer(self, data):
        self.buffer.append(data)  # Adiciona os dados ao buffer

    def read_from_buffer(self):
        if self.buffer:  # Verifica se há dados no buffer
            return self.buffer.pop(0)  # Retorna e remove o primeiro item do buffer
        else:
            return None  # Retorna None se o buffer estiver vazio


# Define a classe AsyncBuffer para operações assíncronas
class AsyncBuffer:
    def __init__(self, size):
        self.size = size  # Define o tamanho do buffer
        self.buffer = []  # Inicializa a lista que armazena os dados do buffer
        self.lock = (
            asyncio.Lock()
        )  # Cria um bloqueio para gerenciar o acesso concorrente ao buffer

    async def write_to_buffer(self, data):
        async with self.lock:  # Adquire o bloqueio de forma assíncrona
            self.buffer.append(data)  # Adiciona os dados ao buffer

    async def read_from_buffer(self):
        async with self.lock:  # Adquire o bloqueio de forma assíncrona
            if self.buffer:  # Verifica se há dados no buffer
                return self.buffer.pop(0)  # Retorna e remove o primeiro item do buffer
            else:
                return None  # Retorna None se o buffer estiver vazio
