from entities.scenario import Scenario
from random import choice, random
import math

class nb_iot:
    def __init__(self, f):
        self.COLLISION_PROBABILITY = 0
        self.ATTENUATION_PROBABILITY = 0
        self.send = f
        self.subcarriers = 48
        self.carrier_bandwidth = 180/self.subcarriers #kHz
        self.subcarriers_per_bands = {
                0: 16,
                1: 16,
                2: 16
            }
        self.bands = {
                0: [5.5547, 5.1152, 4.5234, 3.9023, 3.3223, 2.7305],
                1: [2.4063, 1.9141, 1.4766],
                2: [1.1758, 0.8780, 0.6016, 0.3770, 0.2344, 0.1523]
            }

    def __call__(self, device, pdu = 0):
        scenario = Scenario()
        cell = scenario.getattr('cell')
        self.COLLISION_PROBABILITY = (1/64)*(1 - (63/64)**scenario.getattr('num_devices'))
        #choose a band according to distance from the antenna.
        band = int(device.distance*len(self.bands)/scenario.getattr('config')['nb_iot']['cell_size'])
        self.rapc(device, band, cell)
        p = self.COLLISION_PROBABILITY + self.ATTENUATION_PROBABILITY
        kbps = choice(self.bands[band])*self.carrier_bandwidth
        ec = self.compute_energy_cost(pdu, kbps)
        if random() < p:
            self.send(device, kbps, ec, pdu = pdu)
        self.send(device, kbps, ec, pdu = pdu)

    def rapc(self, device, band, cell):
        traffic = (2^(band)*4*5)/8
        transmission_time = choice([1,2,3])/1000
        energy_consumption = self.dbm_to_mw(23) * transmission_time
        p = math.exp(-cell.bands[band]/self.subcarriers_per_bands[band])
        while random() > p:
            device.generated_traffic += traffic
            device.transmission_time += transmission_time
            device.energy_consumption += energy_consumption
        device.generated_traffic += traffic
        device.transmission_time += transmission_time
        device.energy_consumption += energy_consumption

    def dbm_to_mw(self, value):
        return 10**(value/10)

    def compute_energy_cost(self, value, kbps):
        prx = self.dbm_to_mw(23)
        vdl = kbps*1000
        return (prx*value/vdl)
