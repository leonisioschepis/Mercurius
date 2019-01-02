from entities.scenario import Scenario
from entities.device import send

class tcp:
    def __init__(self, device):
        config = Scenario().getattr('config')
        network_layer = config['scenario']['network_layer']['protocol']
        try:
            occurrences = config['task']['occurrences']
        except KeyError:
            occurrences = 2
        self.header = config['tcp']['standard_header']
        self.keep_alive = config['tcp']['keep_alive']
        self.mss = config['scenario']['max_packet_size'] - self.header - config[network_layer]['standard_header']
        if self.keep_alive:
            self.handshake(device)
            self.communication_time = config['scenario']['time']
            self.keep_alive_time = config['tcp']['keep_alive_ack']
            for i in range(0, (self.communication_time - self.keep_alive_time) * (occurrences - 1), self.keep_alive_time):
                self.heartbeat(device)
            self.handshake(device)

    def heartbeat(self, device):
        send(device)
        send(device)

    def handshake(self, device):
        send(device)
        send(device)
        send(device)

    def send(self, device, pdu):
        if not self.keep_alive:
            self.handshake(device)
            self.handshake(device)
        packet_number = int(pdu / self.mss)
        for i in range(packet_number - 1):
            send(device, self.mss, size = pdu)
        send(device,pdu % (self.mss + 1), size = pdu)
