import asyncio
import logging

logging.basicConfig(filename="buffer_project.log", level=logging.INFO)


def log_message(message):
    logging.info(message)


class CircularBufferSync:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.start = 0
        self.end = 0
        self.full = False

    def write_to_buffer(self, data):
        if self.full:
            raise BufferError("Buffer está cheio")
        self.buffer[self.end] = data
        self.end = (self.end + 1) % self.size
        if self.end == self.start:
            self.full = True

    def read_from_buffer(self):
        if self.start == self.end and not self.full:
            return None
        data = self.buffer[self.start]
        self.buffer[self.start] = None
        self.start = (self.start + 1) % self.size
        self.full = False
        return data


class CircularBufferAsync:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.start = 0
        self.end = 0
        self.full = False
        self.lock = asyncio.Lock()

    async def write_to_buffer(self, data):
        async with self.lock:
            if self.full:
                raise BufferError("Buffer está cheio")
            self.buffer[self.end] = data
            self.end = (self.end + 1) % self.size
            if self.end == self.start:
                self.full = True

    async def read_from_buffer(self):
        async with self.lock:
            if self.start == self.end and not self.full:
                return None
            data = self.buffer[self.start]
            self.buffer[self.start] = None
            self.start = (self.start + 1) % self.size
            self.full = False
            return data
