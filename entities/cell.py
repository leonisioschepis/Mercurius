import logging, uuid

class Cell:
    def __init__(self, size):
        self.id = uuid.uuid1()
        self.devices = list()
        self.size = size
        self.bands = {
            0: 0,
            1: 0,
            2: 0
        }
        logging.info('Cell %s created' %(self.id))

    def __str__(self):
        return "Cell %s, size %s with %s devices" %(self.id, self.size, len(self.devices))

    def add_device(self, device):
        for d in self.devices:
            if getattr(d, 'id') == getattr(device, 'id'):
                logging.error("Cannot exists two devices with the same id")
                exit(409)
        self.devices.append(device)
        self.bands[int(device.distance*len(self.bands)/self.size)] += 1
