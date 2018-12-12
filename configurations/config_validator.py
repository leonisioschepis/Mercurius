import os.path, logging, yaml
from protocols import application_layer, transport_layer, network_layer

CONFIG_DIR = 'configurations'
SIM_CONFIG = 'config.yaml'
METHOD_NAME_FOOTER = "_encapsulation"

def validate_configurations():
    if not os.path.exists(CONFIG_DIR):
        logging.error('DirectoryNotFoundError: Create the directory "configurations" and put the configuration file "config.yaml" inside it.')
        exit()
    if not os.path.exists('%s/%s' %(CONFIG_DIR, SIM_CONFIG)):
        logging.error('FileNotFoundError: The configuration file "config.yaml" must be located in the directory "configurations".')
        exit()
    with open('%s/%s' %(CONFIG_DIR, SIM_CONFIG)) as f:
        config = yaml.load(f)
    if not 'task' in config:
        logging.error('ConfigurationError: the property "task" in the '
        +'configuration file must be set containing the following parameters:'
        +'\n\tMandatory: \n "location" - where the task.py is located.'
        +'\nOptional: \n "occurrences" - the number of executions of the task in'
        +' the given time (default 1).')
        exit()
    if not 'location' in config['task']:
        logging.error('ConfigurationError: the property "task" in the '
        +'configuration file must contain the following parameters:'
        +'\nMandatory: \n "location" - where the task.py is located.'
        +'\nOptional: \n "occurrences" - the number of executions of the task in'
        +' the given time (default 1).')
        exit()
    if not os.path.exists(config['task']['location']):
        logging.error('FileNotFoundError: Please set a valid path for the task.py file')
        exit()
    if not 'occurrences' in config['task']:
        logging.warning('No number of occurrences provided for task. Default setting (1) will be used.')
    if not 'scenario' in config:
        logging.error('ConfigurationError: the property "scenario" in the '
        +'configuration file must contain the following parameters:'
        +'\nMandatory: \n "devices" - Setup about the devices.'
        +'\n"application_layer" - Setup about the application layer'
        +'\n"transport_layer" - Setup about the transport layer'
        +'\n"network_layer" - Setup about the network layer'
        +'\n"link_layer" - Setup about the link layer'
        +'\nOptional: \n - All properties related to protocols')
        exit()
    for layer in ['application_layer', 'transport_layer', 'network_layer', 'link_layer']:
        if not layer in config['scenario']:
            logging.error('ConfigurationError: the property "scenario" in the '
            +'configuration file must contain the following parameters:'
            +'\nMandatory: \n "devices" - Setup about the devices.'
            +'\n"application_layer" - Setup about the application layer'
            +'\n"transport_layer" - Setup about the transport layer'
            +'\n"network_layer" - Setup about the network layer'
            +'\n"link_layer" - Setup about the link layer'
            +'\nOptional: \n - All properties related to protocols')
            exit()
        if not 'protocol' in config['scenario'][layer] or not type(config['scenario'][layer]['protocol']) is str:
            logging.error('ConfigurationError: the property "protocol" must be set up as a string for all layers.')
            exit()
    try:
        application_layer_name = config['scenario']['application_layer']['protocol']
        application_layer_module = __import__('protocols.application_layer.' + application_layer_name, fromlist = [application_layer_name])
        application_layer_class = getattr(application_layer_module, application_layer_name)
    except ImportError:
        logging.error('ClassNotFoundError: there does not exist \'%s\' class in module protocols.application_layer ' %(application_layer_name)
        + 'This can happen due to a typo in the \'config.yaml\' file or because you did not write a class '
        +'application_layer for your custom protocol.')
        exit()
    try:
        transport_layer_name = config['scenario']['transport_layer']['protocol']
        transport_layer_module = __import__('protocols.transport_layer.' + transport_layer_name, fromlist = [transport_layer_name])
        transport_layer_class = getattr(transport_layer_module, transport_layer_name)
    except ImportError:
        logging.error('ClassNotFoundError: there does not exist \'%s\' class in module protocols.transport_layer ' %(transport_layer_name)
        + 'This can happen due to a typo in the \'config.yaml\' file or because you did not write a class '
        +'transport_layer for your custom protocol.')
        exit()
    try:
        network_layer_name = config['scenario']['network_layer']['protocol']
        network_layer_module = __import__('protocols.network_layer.' + network_layer_name, fromlist = [network_layer_name])
        network_layer_class = getattr(network_layer_module, network_layer_name)
    except ImportError:
        logging.error('ClassNotFoundError: there does not exist \'%s\' class in module protocols.network_layer ' %(network_layer_name)
        + 'This can happen due to a typo in the \'config.yaml\' file or because you did not write a class '
        +'network_layer for your custom protocol.')
        exit()
    try:
        link_layer_name = config['scenario']['link_layer']['protocol']
        link_layer_module = __import__('protocols.link_layer.' + link_layer_name, fromlist = [link_layer_name])
        link_layer_class = getattr(link_layer_module, link_layer_name)
    except ImportError:
        logging.error('ClassNotFoundError: there does not exist \'%s\' class in module protocols.link_layer ' %(link_layer_name)
        + 'This can happen due to a typo in the \'config.yaml\' file or because you did not write a class '
        +'link_layer for your custom protocol.')
        exit()
