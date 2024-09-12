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
    fdm.load_model('f16')
    
    fdm.set_dt(DT)
    
    origin = unity.Geolocation(-24.727390,  15.342391, 2000)

    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * m2ft
    fdm[prp.initial_u_fps()] = 700
    fdm[prp.engine_running()] = 1
    
    fdm.run_ic()

    # fdm[prp.turbulence_type()] = TurbulenceTypes.CULP


    client = unity.Client()

    pitch_controller = PIDController()
    roll_controller = PIDController()
    u_controller = PIDController(K_P=1, K_I = 1, K_D = 1)
    
    with client.RenderContext() as ctx:
        
        f16 = unity.GameObject('main-f16', "Aircrafts/F16")
        
        ctx.set_origin(origin)
        ctx.spawn_gameobject(f16, geolocation=origin)
        
        # ctx.draw_axes(
        #     width = 0.05, size = 15,
        #     parent=f16,
        #     transform = unity.Transform(rotation = unity.Vector3(0, -90, 0)),
        #     right_hand=True)

        while True:
            
            roll_rad = 20 * deg2rad * np.sin(4*fdm[prp.sim_time_s()])
            pitch_rad = 10 * deg2rad * np.cos(4 * fdm[prp.sim_time_s()])

            fdm[prp.elevator_cmd()] = -pitch_controller.run_step(pitch_rad, fdm[prp.pitch_rad()])
            fdm[prp.aileron_cmd()] = roll_controller.run_step(0, fdm[prp.roll_rad()])
            # fdm[prp.throttle_cmd()] = u_controller.run_step(700, fdm[prp.u_fps()])
            fdm[prp.throttle_cmd()] = 0.5

            fdm.run()
            
            f16_state = get_aircraft_state_from_fdm(fdm)
            
            f16_state.additional_data = {
                
                # 'U [ft/s]': round(fdm[prp.u_fps()], 2),
                # 'Engine Thrust [lb]': round(fdm[prp.engine_thrust_lbs()], 2),
                # 'Throttle [-]': fdm[prp.throttle_cmd()]
                'x [m]': ctx.get_position(f16).x,
                'y [m]': ctx.get_position(f16).y,
                'z [m]': ctx.get_position(f16).z
            }
            
            
            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    aircrafts = {f16.name: f16_state}),
                time_sleep_s = DT)
        
            

