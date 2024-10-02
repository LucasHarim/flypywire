import os
import sys
import time
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
from flypywire.jsbsim_fdm import properties as prp
from flypywire.control import PIDController
from flight_instruments import AttitudeIndicator

m2ft = 3.281
deg2rad = np.pi/180

def set_ic(fdm, origin: unity.GeoCoordinate):
    
    DT = 0.02
    fdm.set_dt(DT)

    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * m2ft
    fdm[prp.initial_u_fps()] = 100
    fdm[prp.engine_running()] = 1
    fdm[prp.gear()] = 0
    fdm[prp.gear_all_cmd()] = 0.0 ## Landing Gears Up
    
    return fdm


def get_inputs(fdm: jsbsim.FGFDMExec) -> bool:

    # Event handling
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Key press detection
    keys = pygame.key.get_pressed()
    
    #Pause
    # if keys[pygame.K_SPACE]:
    #     fdm.hold()
    #     return True
    
    # Movement controls
    
    if keys[pygame.K_w]:
        fdm[prp.elevator_cmd()] = min(1,max(-1, fdm[prp.elevator_cmd()] + 0.01))
    
    if keys[pygame.K_s]:  # Move down
        fdm[prp.elevator_cmd()] = min(1,max(-1, fdm[prp.elevator_cmd()] - 0.01))
    
    if keys[pygame.K_a]:  # Move left
        fdm[prp.aileron_cmd()] = min(1,max(-1, fdm[prp.aileron_cmd()] - 0.01))
        
    if keys[pygame.K_d]:  # Move right
        fdm[prp.aileron_cmd()] = min(1,max(-1, fdm[prp.aileron_cmd()] + 0.01))

    # Rotation controls
    if keys[pygame.K_q]:  # Rotate counterclockwise
        fdm[prp.rudder_cmd()] = min(1,max(-1, fdm[prp.rudder_cmd()] - 0.01))
    if keys[pygame.K_e]:  # Rotate clockwise
        fdm[prp.rudder_cmd()] = min(1,max(-1, fdm[prp.rudder_cmd()] + 0.01))
    
    return True

if __name__ == '__main__':
    
    fdm = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    fdm2 = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    # fdm.load_model('J3Cub')
    fdm.load_model('f16')
    fdm2.load_model('B747')

    
    origin = unity.GeoCoordinate(-22.951804,  -43.210760, 20000) #Cristo redentor
    fdm = set_ic(fdm, origin)
    fdm.run_ic()
    
    fdm2 = set_ic(fdm2, origin)
    fdm2.run_ic()
    client = unity.Client()
    
    pygame.init()
    clock = pygame.time.Clock()

        # Screen dimensions
    width, height = 300, 300
    screen = pygame.display.set_mode((width, height))
    ai = AttitudeIndicator(width, height)
    pygame.display.set_caption("Attitude Indicator")
    
    with client.RenderContext(False) as ctx:
        
        print(ctx.get_assets_library())
        # main_aircraft = unity.GameObject('main-aircraft', "Airplanes/PiperPA18")
        main_aircraft = unity.GameObject('main-aircraft', "Airplanes/F16")
        side_aircraft = unity.GameObject('side-aircraft','Airplanes/USAF747')

        ctx.set_origin(origin)
        ctx.spawn_gameobject(main_aircraft, geocoordinate=origin)
        
        
        relative_pos = unity.Vector3(5, 10, 50)
        ctx.spawn_gameobject(side_aircraft, transform=unity.Transform(relative_pos, unity.Vector3()), relative_to=main_aircraft)
        
        main_aircraft_state = get_aircraft_state_from_fdm(fdm)
        side_aircraft_state = get_aircraft_state_from_fdm(fdm2)
        # side_aircraft_state = AircraftState(
        #     main_aircraft_state.latitude + 0.001,
        #     main_aircraft_state.longitude + 0.0001,
        #     main_aircraft_state.height_m - 10,
        #     0, 0, 0)
    
        i = 0

        while True:
            
            for f in [fdm, fdm2]:
                if not get_inputs(f):
                    break
                
            
            # if i % 20 == 0:
            #     ctx.freeze_actor(main_aircraft)
            # i += 1

            fdm[prp.throttle_cmd()] = 0.75
            fdm.run()
            fdm2.run()
            
            main_aircraft_state = get_aircraft_state_from_fdm(fdm)
            
            main_aircraft_state.additional_data = {
                'Aileron cmd [0]': round(fdm[prp.aileron_cmd()],2),
                'Rudder cmd [-]': round(fdm[prp.rudder_cmd()], 2),
                'Elevator cmd [-]': round(fdm[prp.elevator_cmd()], 2),
                'Throttle cmd [-]': round(fdm[prp.throttle_cmd()], 2)
            }
            
            
            side_aircraft_state = get_aircraft_state_from_fdm(fdm2) 
            # if fdm[prp.sim_time_s()] < 2:

            #     side_aircraft_state = AircraftState(
            #     main_aircraft_state.latitude + 0.005,
            #     main_aircraft_state.longitude + 0.0001,
            #     main_aircraft_state.height_m + 50,
            #     0, 0, 0)
            # else:
                
            #     side_aircraft_state = AircraftState(
            #         side_aircraft_state.latitude + 5e-5,
            #         side_aircraft_state.longitude,
            #         side_aircraft_state.height_m,
            #         0, 0, 0)
                
            
            aircrafts = {
                main_aircraft.name: main_aircraft_state,
                side_aircraft.name: side_aircraft_state}
            
            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    aircrafts = aircrafts),
                time_sleep_s = 1e-4)
            
            screen.blit(ai.get_screen(fdm[prp.roll_rad()]/deg2rad, fdm[prp.pitch_rad()]/deg2rad), (0,0))

            pygame.display.flip()

            clock.tick(60)
            
        
        # Quit Pygame
        pygame.quit()
        sys.exit()