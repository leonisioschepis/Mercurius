import yaml, logging, os, sys, json
from configurations.config_validator import validate_configurations
from entities.scenario import Scenario
from entities.cell import Cell
from entities.device import Device
from configurations.task import task
from random import randint, choice
import sys
import matplotlib.pyplot as plt

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
config['scenario']['devices']['number'] = int(sys.argv[1])
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

Xs = []
Ys = []
i = 0
results = {}
for device in devices:
    results[i] = {'coordinates': device.coordinates ,'generated_traffic': device.generated_traffic, 'energy_consumption': device.energy_consumption}
    i += 1
    Xs.append(device.coordinates[0])
    Ys.append(device.coordinates[1])
    logging.info('Device %s sent %s bytes in %.4fs consuming %.4f mWs' %(device.id, device.generated_traffic, device.transmission_time, device.energy_consumption))
with open('devices.json', 'w+') as f:
    json.dump(results, f)

fig, ax = plt.subplots()
ax.add_artist(plt.Circle((0, 0), 3000, color = 'r', fill = False))
large = plt.Circle((0, 0), 3000, color = 'r', alpha = 0.2)
ax.add_artist(large)
ax.add_artist(plt.Circle((0, 0), 2000, color = 'w'))
ax.add_artist(plt.Circle((0, 0), 2000, color = 'C1', fill = False))
medium = plt.Circle((0, 0), 2000, color = 'C1', alpha = 0.2)
ax.add_artist(medium)
ax.add_artist(plt.Circle((0, 0), 1000, color = 'w'))
ax.add_artist(plt.Circle((0, 0), 1000, color = 'g', fill = False))
small = plt.Circle((0, 0), 1000, color = 'g', alpha = 0.2)
ax.add_artist(small)
dev = plt.scatter(Xs, Ys, label = "Device", marker = "^", zorder = 10)
antenna = plt.scatter(0,0, label = "Antenna", marker = "p", zorder = 11)
annot = ax.annotate("", xy=(0,0), xytext=(-100,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"), zorder = 12)
annot.set_visible(False)
def update_annot(ind):
    pos = dev.get_offsets()[int(ind["ind"][0])]
    annot.xy = pos
    text = ""
    for i in range(len(ind["ind"])):
        index = int(ind["ind"][i])
        text += "\n---\nCoordinates: (%s,%s)\nGenerated Traffic: %.2f B\nEnergy Consumption: %.2f mWs" %(Xs[index], Ys[index],devices[index].generated_traffic, devices[index].energy_consumption)
    annot.set_text(text[5:])
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = dev.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
fig.canvas.mpl_connect("motion_notify_event", hover)
plt.grid(True)
plt.legend([dev, antenna, small, medium, large], ["Device", "Antenna", "First Band", "Second Band", "Third Band"],
loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3)
plt.savefig('scenario.png')
# plt.show()
logging.info('Scenario plotted')
logging.info('Simulation ended')
