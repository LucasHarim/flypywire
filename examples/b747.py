import os
import jsbsim
import numpy as np
from flypywire import (
    AircraftState,
    SimulationState,
    get_aircraft_state_from_fdm)

import flypywire.unityapi as unity
from flypywire.jsbsim_fdm import properties as prp
from flypywire.jsbsim_fdm.atmosphere import (
    TurbulenceTypes,
    MILSPECWindIntensity,
    MILSPECWindSeverity)

from flypywire.control import PIDController

m2ft = 3.281
deg2rad = np.pi/180

if __name__ == '__main__':
    
    DT = 0.033
    
    fdm = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    fdm.load_model('B747')
    
    fdm.set_dt(DT)
    
    origin = unity.Geolocation(-24.727390,  15.342391, 2000)

    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * m2ft
    fdm[prp.initial_u_fps()] = 700
    # fdm[prp.engine_running()] = 1
    fdm[prp.all_engines_running()] = -1
    fdm.run_ic()

    fdm[prp.turbulence_type()] = TurbulenceTypes.STANDARD


    client = unity.Client()

    pitch_controller = PIDController()
    roll_controller = PIDController()
    
    
    with client.RenderContext() as ctx:
        
        b747 = unity.GameObject('B747', "Aircrafts/USAF747")
        
        ctx.set_origin(origin)
        ctx.spawn_gameobject(b747, geolocation=origin)
        

        while True:
            
            
            fdm[prp.elevator_cmd()] = -pitch_controller.run_step(2 * deg2rad, fdm[prp.pitch_rad()])
            fdm[prp.aileron_cmd()] = roll_controller.run_step(roll_rad, fdm[prp.roll_rad()])
            fdm[prp.throttle_cmd()] = 0.75

            fdm.run()
            
            b747_state = get_aircraft_state_from_fdm(fdm)
            
            b747_state.additional_data = {
                "u [ft/s]": round(fdm[prp.u_fps()], 2),
                "Thrust [lb]": round(fdm[prp.engine_thrust_lbs()], 2)
            }

            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    aircrafts = {b747.name: b747_state}),
                time_sleep_s = DT)
        
            

