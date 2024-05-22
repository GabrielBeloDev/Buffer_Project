import asyncio


class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    def write_to_buffer(self, data):
        self.buffer.append(data)

    def read_from_buffer(self):
        if self.buffer:
            return self.buffer.pop(0)
        else:
            return None


class AsyncBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.lock = asyncio.Lock()

    async def write_to_buffer(self, data):
        async with self.lock:
            self.buffer.append(data)

    async def read_from_buffer(self):
        async with self.lock:
            if self.buffer:
                return self.buffer.pop(0)
            else:
                return None
