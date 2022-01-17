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


def on_release(key, mc):
    if key == keyboard.Key.esc:
        # Stop listener
        print('all done')
        return False
    if key == keyboard.Key.up:
        mc.up(DEFAULT_HEIGHT)
    elif key == keyboard.Key.down:
        mc.down(DEFAULT_HEIGHT)            
    elif key == keyboard.KeyCode.from_char('w'):
        mc.forward(DEFAULT_TRANSLATE)            
    elif key == keyboard.KeyCode.from_char('s'):
        mc.back(DEFAULT_TRANSLATE)
    elif key == keyboard.KeyCode.from_char('a'):
        mc.left(DEFAULT_TRANSLATE)
    elif key ==keyboard.KeyCode.from_char('d'):
        mc.right(DEFAULT_TRANSLATE)


def param_deck_flow(name, value_str):
    value = int(value_str)
    global is_deck_attached
    if value:
        is_deck_attached = True
    else:
        is_deck_attached = False


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)
        if is_deck_attached:
            print('let\'s fly')
            with MotionCommander(scf, default_height=0.5) as mc:
                with keyboard.Listener(on_release=lambda event:on_release(event, mc)) as listener:
                    listener.join()
                    print('waiting...')
            print('failing here')
