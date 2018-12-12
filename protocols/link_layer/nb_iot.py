from entities.scenario import Scenario
from random import choice, random
import math
class nb_iot:
    def __init__(self, f):
        self.send = f
        self.carrier_bandwidth = 180 #kHz
        self.bands = {
                0: [5.5547, 5.1152, 4.5234, 3.9023, 3.3223, 2.7305],
                1: [2.4063, 1.9141, 1.4766],
                2: [1.1758, 0.8780, 0.6016, 0.3770, 0.2344, 0.1523]
            }

    def __call__(self, device, pdu = 0):
        scenario = Scenario()
        cell = scenario.getattr('cell')
        #choose a band according to distance from the antenna.
        band = int(device.distance*len(self.bands)/scenario.getattr('config')['nb_iot']['cell_size'])
        p = math.exp(-cell.bands[band]/16)
        kbps = choice(self.bands[band])*self.carrier_bandwidth
        #print('This device communicate at %.2f kbps' %(bps))
        ec = self.compute_energy_cost(pdu, kbps)
        while random() > p:
            self.send(device, kbps, ec, pdu = pdu)
        self.send(device, kbps, ec, pdu = pdu)

    def dbm_to_mw(self, value):
        return 10**(value/10)

    def compute_energy_cost(self, value, kbps):
        prx = self.dbm_to_mw(23)
        vdl = kbps*1000
        return (prx*value/vdl)
