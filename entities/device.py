import logging, uuid, threading, time
from entities.scenario import Scenario
from protocols.link_layer.nb_iot import nb_iot
from random import randint

class WorkingDevice (threading.Thread):
    def __init__(self, threadID, dev):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.device = dev

    def run(self):
        logging.info("Starting device " + str(getattr(self.device,'id')))
        scenario = Scenario()
        #LOADING APPLICATION LAYER
        application_layer_name = scenario.getattr('application_layer')
        application_layer_module = __import__('protocols.application_layer.' + application_layer_name, fromlist = [application_layer_name])
        application_layer_class = getattr(application_layer_module, application_layer_name)
        #LOADING TRANSPORT LAYER
        transport_layer_name = scenario.getattr('transport_layer')
        transport_layer_module = __import__('protocols.transport_layer.' + transport_layer_name, fromlist = [transport_layer_name])
        transport_layer_class = getattr(transport_layer_module, transport_layer_name)
        transport_layer = transport_layer_class(self.device)
        for i in range(scenario.getattr('config')['task']['occurrences']):
            task_result = self.device.task()
            application_layer = application_layer_class(task_result, self.device.auth)
            traffic = application_layer.get_cost()
            transport_layer.send(self.device, traffic)
        logging.info("Stopping device "  + str(getattr(self.device,'id')))

class Device:
    def __init__(self, max_distance, f, auth = False):
        self.id = uuid.uuid1()
        self.auth = auth
        self.distance = randint(0,max_distance)
        self.task = f
        self.generated_traffic = 0
        self.transmission_time = 0
        self.energy_consumption = 0
        self.thread = None
        logging.info('Device %s created' %(self.id))

    def reset(self):
        self.generated_traffic = 0
        logging.info('Device %s reset' %(self.id))

    def run(self):
        self.thread = WorkingDevice(self.id, self)
        self.thread.start()

@nb_iot
def send(device, bps, ec, pdu = 0):
    scenario = Scenario()
    #LOADING NETWORK LAYER
    network_layer_name = scenario.getattr('network_layer')
    network_layer_module = __import__('protocols.network_layer.' + network_layer_name, fromlist = [network_layer_name])
    network_layer_class = getattr(network_layer_module, network_layer_name)
    datagram = pdu
    datagram += scenario.getattr('config')[scenario.getattr('transport_layer')]['standard_header']
    datagram = network_layer_class().get_cost(datagram)
    device.generated_traffic += datagram
    device.transmission_time += datagram/(bps*1000)
    device.energy_consumption += ec
    return datagram
