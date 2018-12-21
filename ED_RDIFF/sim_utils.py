import queue

class Packet:
    def __init__(self, identifier,cost, block_size,diffs):
        self.id = identifier
        self.cost = cost
        self.block_size = block_size
        self.diffs = diffs

class Sensor:
    def __init__(self, identifier):
        self.id = identifier
        self.queue = queue.Queue(maxsize = 1)

class Buffer:
    def __init__(self):
        self.max_size = 1024
        self.size = 0
        self.container = {}

    def empty(self):
        return self.size == 0

    def to_string(self):
        return self.container

    def clean(self):
        self.size = 0
        self.container = {}
