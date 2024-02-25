from pathlib import Path
try: import readline
except ModuleNotFoundError: pass
import readchar
from readchar import key
from sound_lib import output, stream
from . import carts
from . import config
devices = []
o = output.Output()
def init():
    global devices
    print(config.load())
    print('initializing output...')
    o.device = config.device
    print('Getting device names.')
    devices = o.get_device_names()
    print(f'Device set to {devices[config.device-1]}.')
    print('Loading carts.')
    print(carts.load(config.cart_set))

def change_device():
    global o
    print('Select from the following devices.')
    for i, device in enumerate(devices): print(f'{i+1}. {device}')
    while True:
        print('Device?')
        keycode = readchar.readkey()
        try:
            if int(keycode) in range(1, len(devices)+1):
                selected = int(keycode)
                o.device = selected
                print(f'Device set to {devices[selected-1]}.')
                config.device = selected
                break
        except ValueError:
            print('Not a number, returning to main menu.')
            break
        else:
            print('Invalid device number.')

def review_config():
    print('This is the current configuration.')
    print(f'The current device is {config.device}. {devices[config.device-1]}.')
    print(f'The current cart set is {config.cart_set}.')
    
def list_carts():
    print('These are your current carts.')
    print(carts.list())

def edit_cart():
    cart = carts.get(carts.selected)
    print('Here are the settings for the current cart. To leave a setting unchanged, just press enter.')
    path = input(f'File or directory for this cart? Currently {cart.path}.')
    title = input(f'Title of this cart? Currently {cart.title}.')
    random = input(f'Do you want this cart to be in random mode? The random mode is currently {cart.random}.')
    cart.title = title if title else cart.title
    cart.path = Path(path) if path else cart.path
    yeses = ['true', 'y', 'yes', '1', 'yeah', 'yep']
    if random == '': random = cart.random
    elif random in yeses: random = True
    else: random = False
    cart.random = random
    print('here is the updated cart.')
    print(cart)
    cart.update_files()

def change_cart_set():
    file = input(f'Cart set to load? Currently {config.cart_set}. ')
    if file == '': print('leaving cart set unchanged.')
    else:
        while True:
            print('Keep existing carts in memory, if cart set not found? Y/N')
            keep_carts = False
            keycode = readchar.readkey()
            if keycode == 'y': keep_carts = True; break
            elif keycode == 'n': keep_carts = False; break
            else: print('Invalid choice, try again.')
        print(carts.load(file, load_defaults=False, keep_carts=keep_carts))

def previous_cart():
    if carts.selected == 1: print('Already at first cart.')
    else: carts.selected -= 1
    print(f'selected. {carts.get(carts.selected)}')

def next_cart():
    if carts.selected == 12: print('Already at last cart.')
    else: carts.selected += 1
    print(f'selected. {carts.get(carts.selected)}')

def run():
    init()
    cart_keys = {}
    for i in range(1, 10): cart_keys[str(i)] = i
    cart_keys['0'] = 10
    cart_keys['-'] = 11
    cart_keys['='] = 12
    cart_stop_keys = {}
    for i, c in enumerate('!@#$%^&*()_+'): cart_stop_keys[c] = i+1
    cart_stop_keys['"'] = 2 # for shift-2 on UK keyboard. quote sign.
    cart_stop_keys[chr(163)] = 3 # for shift-3 on UK keyboard (pound symbol)
    print('ArfCart is ready.')
    print('Please select from the following.')
    print('1-0, dash, and equals. play a cart. Add shift to stop')
    print('Grave accent. Change cart set.')
    print('C. clear selected cart.')
    print('d. Change device')
    print('E. Edit currently selected cart.')
    print('L. List carts.')
    print('Q or escape. quit')
    print('R. Review config.')
    print('left/right arrow. change selected cart.')
    print("Up/Down arrow. adjust selected cart's volume")
    print(f'Selected. {carts.get(carts.selected)}')
    while True:
        keycode = readchar.readkey()
        if keycode in cart_keys: print(carts.play(cart_keys[keycode]))
        elif keycode in cart_stop_keys: print(carts.stop(cart_stop_keys[keycode]))
        elif keycode == 'c': clear_cart()
        elif keycode == '`': change_cart_set()
        elif keycode == 'd': change_device()
        elif keycode == 'e': edit_cart()
        elif keycode == 'l': list_carts()
        elif keycode == 'q' or keycode == key.ESC: break
        elif keycode == 'r': review_config()
        elif keycode == key.LEFT: previous_cart()
        elif keycode == key.RIGHT: next_cart()
        else: print('Invalid choice')
    print('closing the cart machine...')
    print(carts.save(config.cart_set))
    print(config.save())

if __name__ == "__main__": sys.exit(run())