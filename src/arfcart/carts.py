from . import config
from arfcart.config import config_path
import configparser
import os
from pathlib import Path
import random
from sound_lib import output, stream
from sound_lib.main import BassError

selected = 1
one_shot = 0
continuous = 1
class Cart:
    def __init__(self, number: int, path='', title='Empty Cart', random=False, mode=one_shot):
        self.number = number
        self.title = title
        self.files = []
        self.random = random
        self.path = Path(path)
        self.mode = mode
        self.volume = 1.0
        self.update_files()
        
    def __str__(self):
        result = f'{self.number}. {self.title}: {self.path}: '
        result += 'random ' if self.random else 'sequential '
        result += 'one-shot. ' if self.mode == one_shot else 'continuous. '
        return result
    
    def update_files(self):
        if self.path.is_dir() and str(self.path) != '.':
            found_files = self.path.rglob('*.*')
            self.files = [str(file) for file in found_files if file.suffix in config.extensions]
            self.files.sort()
            self.file_in_list = iter(self.files) # for sequential playback mode.
        else: self.files = []
    
    def play(self):
        if hasattr(self, 'stream'): del(self.stream)
        if str(self.path) == '' or str(self.path) == '.': return f'Cart {self.number} is empty.'
        if len(self.files) == 0: file = str(self.path)
        elif self.random: file = random.choice(self.files)
        else:
            try:
                file = next(self.file_in_list)
            except StopIteration:
                self.file_in_list = iter(self.files)
                file = next(self.file_in_list)
        try:
            self.stream = stream.FileStream(file=file)
        except BassError as err:
            return f'Error while attempting to load {file} from {self.title}. {err}'
        self.stream.volume = self.volume
        self.stream.play(True)
        return self.title

    def stop(self):
        if hasattr(self, 'stream'): self.stream.stop(); return 'stopped'
        else: return f'Cart {self.number} is empty'

def _create_default_carts():
    result = []
    for i in range(1, 13): result.append(Cart(i))
    return result

carts = []
def _load_default_carts(file):
    global carts
    messages = []
    c = configparser.ConfigParser()
    if len(c.read(os.path.join(config_path, 'default.ccarts'))) == 0:
        carts = _create_default_carts()
        messages.append('Default cart set not found, creating new default carts.')
        config.cart_set = 'default'
    else:
        for i in range(1, 13):
            title = c[f'cart{i}']['title']
            path = c[f'cart{i}']['path']
            random = c[f'cart{i}'].getboolean('random')
            carts.append(Cart(i, path, title, random))
        messages.append(f'Loaded default carts in place of  {file}.')
    return messages

def load(file, load_defaults=True, keep_carts=True):
    global carts
    messages = []
    c = configparser.ConfigParser()
    if len(c.read(os.path.join(config_path, file + '.carts'))) == 0:
        messages.append(f'Specified cart set {file} not found or could not be read. ')
        if load_defaults:
            messages.append('Loading default carts.')
            messages.extend(_load_default_carts(file))
        else:
            config.cart_set = file
            if keep_carts:
                messages.append(f'Cart set now set to {file}, with existing carts still in memory.')
                return messages
            else:
                messages.append('Creating a new set of empty carts.')
                carts = _create_default_carts()
                return messages
    else:
        config.cart_set = file
        carts.clear()
        for i in range(1, 13):
            title = c[f'cart{i}']['title']
            path = c[f'cart{i}']['path']
            random = c[f'cart{i}'].getboolean('random')
            carts.append(Cart(i, path, title, random))
        messages.append(f'Loaded carts from {file}.')
    return messages

def save(file):
    c = configparser.ConfigParser()
    for cart in carts:
        c.add_section(f'cart{cart.number}')
        c[f'cart{cart.number}']['title'] = cart.title
        c[f'cart{cart.number}']['path'] = str(cart.path)
        c[f'cart{cart.number}']['random'] = str(cart.random)
    with open(os.path.join(config_path, file + '.carts'), 'w') as f: c.write(f)
    return f'Carts saved to {file}'

def play(number): return carts[number-1].play()
def stop(number): return carts[number-1].stop()

def list():
    result = ""
    for cart in carts: result += str(cart) + '\n'
    return result

def get(number): return carts[number-1]
