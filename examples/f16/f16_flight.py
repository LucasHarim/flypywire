import numpy as np
from flypywire import (
    ActorState,
    SimulationState,
    get_aircraft_state_from_fdm)

import flypywire.unityapi as unity
from flypywire.jsbsim_fdm import properties as prp
from flypywire import aircrafts
from flypywire.jsbsim_fdm.atmosphere import (
    TurbulenceTypes,
    MILSPECWindIntensity,
    MILSPECWindSeverity)

from flypywire.control import PIDController
from events import event_sequence


m2ft = 3.281
deg2rad = np.pi/180
DT = 0.03

if __name__ == '__main__':
    
    aircraft = aircrafts.F16

    origin = unity.GeoCoordinate(-24.727390,  15.342391, 8000) ##Namibia
    fdm = aircraft.fdm_cruise(origin)
    fdm.set_dt(DT)
    
    mission = event_sequence(fdm, get_aircraft_state_from_fdm(fdm))
    
    client = unity.Client()

    pitch_controller = PIDController(dt = DT)
    roll_controller = PIDController(K_P = 1, dt = DT)
    u_controller = PIDController(K_P=1, K_I = 1, K_D = 1, dt = DT)
    
    with client.RenderContext() as ctx:
        
        for a in ctx.get_assets_library():
            print(a)

        ctx.set_origin(origin)
        
        
        asset = aircraft.get_asset('main-aircraft')
        ctx.spawn_gameobject(asset, geocoordinate=origin)
        
        ctx.draw_axes(parent = asset, size = 10, right_hand=True)

        while True:
            
            mission.tick()
            
            fdm[prp.throttle_cmd()] = 0.75
            
            fdm.run()
            f16_state = get_aircraft_state_from_fdm(fdm)
            
            f16_state.additional_data = {
                'Heading [deg]': round(fdm[prp.heading_deg()], 3)
            }

            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    actors =  {asset.name: f16_state}),
                time_sleep_s = 2e-5)
            
            