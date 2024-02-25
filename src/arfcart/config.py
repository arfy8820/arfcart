# configuration module.
import configparser
import os
from platform_utils import paths
# default config values.
device = 1 # default device
cart_set = 'default'
extensions = '.aac .aif .aiff .alac .flac .m4a .mp1 .mp2 .mp3 .ogg .opus .wav'.split()
config_path = paths.app_data_path('arfcart')
main_config = os.path.join(config_path, 'arfcart.cfg')
paths.prepare_app_data_path('arfcart')
def load():
    global device, cart_set
    config = configparser.ConfigParser()
    if len(config.read(main_config)) == 0: return 'Main configuration not found, creating...'
    device = config['arfcart'].getint('device')
    cart_set = config['arfcart']['carts']
    return 'Main configuration loaded'

def save():
    config = configparser.ConfigParser()
    config.add_section('arfcart')
    config['arfcart']['device'] = str(device)
    config['arfcart']['carts'] = cart_set
    with open(main_config, 'w') as configfile: config.write(configfile)
    return 'Configuration saved.'

