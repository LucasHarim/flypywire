import os
import sys
import time
import argparse
import jsbsim
import numpy as np
import pygame
from flypywire import (
    AircraftState,
    SimulationState,
    get_aircraft_state_from_fdm)

from flypywire.jsbsim_fdm.atmosphere import (
    TurbulenceTypes,
    MILSPECWindIntensity,
    MILSPECWindSeverity)

import flypywire.unityapi as unity
from flypywire import aircrafts
from flypywire.jsbsim_fdm import properties as prp
from flypywire.control import PIDController
from flight_instruments import AttitudeIndicator

m2ft = 3.281
deg2rad = np.pi/180

pygame.init()
pygame.joystick.init()
# Check for joystick(s) and initialize them
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected")
    pygame.quit()
    sys.exit()

def get_inputs(fdm: jsbsim.FGFDMExec) -> bool:

    # Event handling
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    
    offset_x = 0.0185
    offset_y = -0.013
    axis_x = joystick.get_axis(0)  # Left/Right on stick
    axis_y = joystick.get_axis(1)  # Up/Down on stick

    fdm[prp.aileron_cmd()] = axis_x + offset_x
    fdm[prp.elevator_cmd()] = -(axis_y + offset_y)
    
    
    return True

def start_sim(aircraft: aircrafts.AircraftTemplate, origin: unity.GeoCoordinate):
    
    fdm = aircraft.fdm_cruise(origin)

    client = unity.Client()
    
    
    clock = pygame.time.Clock()

    # Screen dimensions
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    ai = AttitudeIndicator(width, height)
    pygame.display.set_caption("Attitude Indicator")
    
    with client.RenderContext() as ctx:
        
        assets = ctx.get_assets_library()
        for a in assets: 
            print(a)
        
        ctx.set_origin(origin)

        main_aircraft = aircraft.get_asset('main-aircraft')
        ctx.spawn_gameobject(main_aircraft, geocoordinate=origin)
        
        main_aircraft_state = get_aircraft_state_from_fdm(fdm)

        while True:
            
            if not get_inputs(fdm):
                break

            fdm[prp.throttle_cmd()] = 0.75
            fdm.run()
            
            main_aircraft_state = get_aircraft_state_from_fdm(fdm)
            
            main_aircraft_state.additional_data = {
                'Aileron cmd [0]': round(fdm[prp.aileron_cmd()],2),
                'Rudder cmd [-]': round(fdm[prp.rudder_cmd()], 2),
                'Elevator cmd [-]': round(fdm[prp.elevator_cmd()], 2),
                'Throttle cmd [-]': round(fdm[prp.throttle_cmd()], 2)
            }
            
            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    aircrafts = {main_aircraft.name: main_aircraft_state}),
                time_sleep_s = 1e-4)
            
            screen.blit(ai.get_screen(fdm[prp.roll_rad()]/deg2rad, fdm[prp.pitch_rad()]/deg2rad), (0,0))

            pygame.display.flip()

            clock.tick(60)
            
        
        # Quit Pygame
        pygame.quit()
        sys.exit()
    
if __name__ == '__main__':
    
    _aircraft_list = ''
    
    for name in aircrafts.aircraft_collection.keys():
        _aircraft_list += f'{name}\n'

    parser = argparse.ArgumentParser('Joystick-Flight')
    parser.add_argument('-a', '--aircraft', help = f'Select one of the following aircrafts: {_aircraft_list}')
    
    args = parser.parse_args()
    origin = unity.GeoCoordinate(-22.951804,  -43.210760, 1000) #Cristo redentor
    
    start_sim(aircrafts.aircraft_collection[args.aircraft], origin)
    
    