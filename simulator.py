import yaml, logging, os, sys
from configurations.config_validator import validate_configurations
from entities.scenario import Scenario
from entities.cell import Cell
from entities.device import Device
from configurations.task import task

CONFIG_DIR = 'configurations'
SIM_CONFIG = 'config.yaml'

#logging configurations
try:
    os.remove("simulation.log")
except FileNotFoundError:
    pass
fileHandler = logging.FileHandler('simulation.log')
streamHandler = logging.StreamHandler(sys.stdout)
logging.basicConfig(format = '%(asctime)s [%(filename)-12.12s] [%(levelname)-5.5s]  %(message)s',
                    handlers = [fileHandler,streamHandler],
                    level = logging.DEBUG)

validate_configurations()
#Load configurations
logging.info('Loading configurations')
with open('%s/%s' %(CONFIG_DIR, SIM_CONFIG)) as f:
    config = yaml.load(f)

#Setting up the scenario
scenario = Scenario()
logging.debug('Number of devices: %s' %(config['scenario']['devices']['number']))
scenario.setattr('num_devices', config['scenario']['devices']['number'])
scenario.setattr('application_layer',config['scenario']['application_layer']['protocol'])
scenario.setattr('transport_layer',config['scenario']['transport_layer']['protocol'])
scenario.setattr('network_layer',config['scenario']['network_layer']['protocol'])
scenario.setattr('link_layer',config['scenario']['link_layer']['protocol'])
scenario.setattr('config', config)
logging.debug(scenario)

#Setting up the cell
cell = Cell(config[scenario.getattr('link_layer')]['cell_size'])
scenario.setattr('cell', cell)
for i in range(scenario.getattr('num_devices')):
    try:
        device = Device(getattr(cell, 'size'), task, config[scenario.getattr('application_layer')]['authentication'])
    except KeyError:
        device = Device(getattr(cell, 'size'), task)
    cell.add_device(device)
logging.debug(cell)

devices = getattr(cell, 'devices')

for device in devices:
    device.run()

for device in devices:
    device.thread.join()

for device in devices:
    logging.debug('Device %s sent %s bytes in %.4fs consuming %.4f mWs' %(device.id, device.generated_traffic, device.transmission_time, device.energy_consumption))
logging.info('Simulation ended')
