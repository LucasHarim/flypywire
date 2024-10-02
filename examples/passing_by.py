import os
import time
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
ft2mt = 0.3048
DT = 0.01

if __name__ == '__main__':
    
    
    
    fdm = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    fdm.load_model('f16')
    
    fdm.set_dt(DT)
    
    origin = unity.GeoCoordinate(-24.727390,  15.342391, 2000)

    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * m2ft
    fdm[prp.initial_u_fps()] = 700
    fdm[prp.engine_running()] = 1
    
    fdm.run_ic()

    fdm[prp.turbulence_type()] = TurbulenceTypes.STANDARD


    client = unity.Client()
    
    pitch_controller = PIDController(1, 1, 1)
    roll_controller = PIDController()
    u_controller = PIDController(K_P=1, K_I = 1000, K_D = 1)
    
    with client.RenderContext() as ctx:
        
        print(ctx.get_assets_library())
        
        f16 = unity.GameObject('main-f16', "Airplanes/F16")
        b747 = unity.GameObject('787-tank', "Airplanes/USAF747")
        

        ctx.set_origin(origin)

        ctx.spawn_gameobject(f16, geocoordinate=origin)
        
        # ctx.draw_axes(size = 15, width=0.1, parent=f16, transform = unity.Transform(rotation = unity.Vector3(0, -90, 0)),right_hand=True)

        relative_pos = unity.Vector3(5, 10, 50)
        ctx.spawn_gameobject(b747, transform=unity.Transform(relative_pos, unity.Vector3()), relative_to=f16)
        
        f16_state = get_aircraft_state_from_fdm(fdm)
        

        b747_state = AircraftState(
                f16_state.latitude + 0.001,
                f16_state.longitude + 0.0001,
                f16_state.height_m + 10,
                roll_rad = 0,
                pitch_rad = 0,
                yaw_rad = 0
            )
        
        while True:
            
            fdm[prp.elevator_cmd()] = -pitch_controller.run_step(2 * deg2rad, fdm[prp.pitch_rad()])
            fdm[prp.aileron_cmd()] = roll_controller.run_step(0, fdm[prp.roll_rad()])
            fdm[prp.throttle_cmd()] = u_controller.run_step(700, fdm[prp.u_fps()])

            
            # f16_relative_pos = ctx.get_position(f16)
            

            f16_state = get_aircraft_state_from_fdm(fdm)
            f16_state.additional_data = {
                prp.u_fps(): f'{round(fdm[prp.u_fps()], 1)} ft/s',
                prp.engine_thrust_lbs(): fdm[prp.engine_thrust_lbs()],
                prp.throttle_cmd(): fdm[prp.throttle_cmd()],
                
                # 'x':  f16_relative_pos.x,
                # 'y':  f16_relative_pos.y,
                # 'z':  f16_relative_pos.z
            }
        
            
            b747_state = AircraftState(
                b747_state.latitude + 2e-5,
                b747_state.longitude,
                b747_state.height_m,
                0, 0, 0)
            
            fdm.run()

            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    aircrafts = {
                        f16.name: f16_state,
                        b747.name: b747_state}
                    ), 
                time_sleep_s = 1e-5)
        
            

