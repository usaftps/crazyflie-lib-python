import curses
import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
DEFAULT_HEIGHT = 0.1
is_deck_attached = False
position_estimate = [0, 0]

logging.basicConfig(level=logging.ERROR)


def keyboard_inputs(stdscr):
    stdscr.addstr('Hello world')
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            if c == 27:
                break
            elif c == 259:
                stdscr.addstr('up arrow')
            elif c == 258:
                stdscr.addstr('down arrow')
            elif c == 119:
                stdscr.addstr('w key to go forward')
            elif c == 115:
                stdscr.addstr('s key to go backward')
            elif c == 97:
                stdscr.addstr('a key to translate left')
            elif c == 100:
                stdscr.addstr('d key to translate right')
            # print numeric value
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            # return curser to start position
            stdscr.move(0, 0)

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
    #curses.wrapper(keyboard_inputs, scf)
    cflib.crtp.init_drivers()
    '''
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
    '''
    time.sleep(1)
    if not is_deck_attached:
        curses.wrapper(keyboard_inputs)
    print("and out")

