import math
import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.utils.power_switch import PowerSwitch

ITERATIONS = 3

uris = [
    'radio://0/20/2M/E7E7E7E700',
    'radio://0/20/2M/E7E7E7E701',
    'radio://0/20/2M/E7E7E7E702',
    'radio://0/20/2M/E7E7E7E703',
    'radio://0/20/2M/E7E7E7E704',
    'radio://0/20/2M/E7E7E7E705',
    'radio://0/20/2M/E7E7E7E706',
]

phase = 0


def activate_high_level_commander(scf):
    scf.cf.param.set_value('commander.enHighLevel', '1')


def get_height(scf):
    pos = uris.index(scf.cf.link_uri)
    where = (pos + phase) % 6
    return 1 + 0.6 * math.sin(where * math.pi / 6.0)


def take_off(scf):
    h = get_height(scf)
    scf.cf.commander.send_setpoint(0, 0, 0, 0)
    time.sleep(0.1)

    scf.cf.high_level_commander.takeoff(h, 5.0)
    time.sleep(2.5)


def land(scf, pos):
    scf.cf.high_level_commander.go_to(pos.x, pos.y, 0.2, 0, 7.0)
    time.sleep(7)
    scf.cf.high_level_commander.land(0, 1.0)
    time.sleep(1.5)
    scf.cf.high_level_commander.stop()
    time.sleep(0.5)


def wave(scf, pos):
    h = get_height(scf)
    scf.cf.high_level_commander.go_to(pos.x, pos.y, h, 0, 1.0)


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')

    print('Reseting all in swarm ...')
    for uri in uris:
        switch = PowerSwitch(uri)
        switch.stm_power_cycle()
        switch.close()

    print('Connecting ...')
    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel_safe(activate_high_level_commander)

        print('Reset estimators and wait for position ...')
        swarm.reset_estimators()

        print('Getting estimated positions ...')
        positions = swarm.get_estimated_positions()
        uris.sort(key=lambda uri: positions[uri].y)

        print('Sending take off ...')
        swarm.sequential(take_off)
        time.sleep(3)

        # The `args_dict` arg to the swarm methods expect a dictonary layout:
        #   {
        #       URI: [list, of, params]
        #   }
        #
        # So we turn the positions dictonary from { URI: SwarmPosition } to
        # { URI: [SwarmPosition] }
        parameters = {key: [value] for (key, value) in positions.items()}

        print('Starting wave ...')
        while phase < ITERATIONS * (2 * math.pi / (math.pi / 6)):
            swarm.parallel_safe(wave, args_dict=parameters)
            time.sleep(0.6)
            phase += 1

        print('Going in for landing ...')
        swarm.parallel_safe(land, args_dict=parameters)
