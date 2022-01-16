import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.utils import uri_helper
from pynput import keyboard

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
DEFAULT_HEIGHT = 0.05
DEFAULT_TRANSLATE = 0.05
is_deck_attached = False
position_estimate = [0, 0]

logging.basicConfig(level=logging.ERROR)


def on_release(key, scf):
    '''
    print('{0} released'.format(key))
    '''
    with MotionCommander(scf, default_height=0.5) as mc:
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        if key == keyboard.Key.up:
            print('up arrow, go up')
            mc.up(DEFAULT_HEIGHT)
        elif key == keyboard.Key.down:
            print('down arrow, go down')
            mc.down(DEFAULT_HEIGHT)            
        elif key == keyboard.KeyCode.from_char('w'):
            print('w, go forwards')
            mc.forward(DEFAULT_TRANSLATE)            
        elif key == keyboard.KeyCode.from_char('s'):
            print('s, go backward')
            mc.back(DEFAULT_TRANSLATE)
        elif key == keyboard.KeyCode.from_char('a'):
            print('a, go left')
            mc.left(DEFAULT_TRANSLATE)
        elif key ==keyboard.KeyCode.from_char('d'):
            print('d, go right')
            mc.right(DEFAULT_TRANSLATE)


def keyboard_test():
    a=1

def keyboard_inputs(scf):
    print("get keyboard inputs")
    with MotionCommander(scf, default_height=.5) as mc:
        time.sleep(2)
        while True:
            key_pressed = keyboard.read_key()
            if keyboard.is_pressed('esc'):
                mc.stop()
                print('All done!')
                break
            if key_pressed == keyboard.KEY_UP:
                print('up arrow')
                mc.up(DEFAULT_HEIGHT)
            elif key_pressed == keyboard.KEY_DOWN:
                print('down arrow')
                mc.down(DEFAULT_HEIGHT)
            elif key_pressed == 'w':
                print('w key to go forward')
                mc.forward(DEFAULT_TRANSLATE)
            elif key_pressed == 's':
                print('s key to go backward')
                mc.forward(DEFAULT_TRANSLATE)
            elif key_pressed == 'a':
                print('a key to translate left')
                mc.forward(DEFAULT_TRANSLATE)
            elif key_pressed == 'd':
                print('d key to translate right')
                mc.forward(DEFAULT_TRANSLATE)                


def param_deck_flow(name, value_str):
    value = int(value_str)
    print(value)
    global is_deck_Attached
    if value:
        is_deck_attached = True
        print("deck attached")
    else:
        is_deck_attached = False
        print("deck NOT attached")


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
    time.sleep(2)

    if is_deck_attached:
        with keyboard.Listener(on_release=lambda event:on_release(event, scf)) as listener:
            listener.join()
        print('failing here')
