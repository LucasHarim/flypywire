import os
import jsbsim
import numpy as np
import time
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
from events import event_sequence


m2ft = 3.281
deg2rad = np.pi/180

if __name__ == '__main__':
    
    DT = 0.02
    
    fdm = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    fdm.load_model('f16')
    
    fdm.set_dt(DT)
    
    # origin = unity.GeoCoordinate(46.536804,  7.962639, 8000) ##Alps
    # origin = unity.GeoCoordinate(-2.4859385, -43.128407, 8000) ## Lensois
    origin = unity.GeoCoordinate(-24.727390,  15.342391, 8000) ##Namibia
    

    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * m2ft
    fdm[prp.initial_u_fps()] = 800
    fdm[prp.engine_running()] = 1
    fdm[prp.gear()] = 0
    fdm[prp.gear_all_cmd()] = 0.0 ## Landing Gears Up
    
    fdm.run_ic()
    
    mission = event_sequence(fdm, get_aircraft_state_from_fdm(fdm))
    # fdm[prp.turbulence_type()] = TurbulenceTypes.CULP
    
    client = unity.Client()

    pitch_controller = PIDController(dt = DT)
    roll_controller = PIDController(K_P = 1, dt = DT)
    u_controller = PIDController(K_P=1, K_I = 1, K_D = 1, dt = DT)
    
    with client.RenderContext(False) as ctx:
        
        print(ctx.get_assets_library())
        f16 = unity.GameObject('main-f16', "Airplanes/JAS39Gripen")
        
        ctx.set_origin(origin)
        ctx.spawn_gameobject(f16, geocoordinate=origin)
        
        # axes = ctx.draw_axes(
        #     width = 0.05, size = 15,
        #     parent=f16,
        #     transform = unity.Transform(rotation = unity.Vector3(0, -90, 0)),
        #     lifetime= -1,
        #     right_hand=True)
        
        # ctx.spawn_camera('main-cam', f16, transform=unity.Transform(position = unity.Vector3(0, 1.2, 0)))
        
        # fdm['fcs/fbw-override'] = 1
        # ctx.draw_actor_trail(f16.name, 0.1, unity.Color(0, 0, 1), unity.Color(1, 0, 0))

        t_freeze = 1
        i = 0

        while True:
            
            
            mission.tick()
            
            fdm[prp.throttle_cmd()] = 0.75
            
            fdm.run()
            if (i % 5 == 0 and fdm[prp.sim_time_s()] < 20):
            # if (np.isclose(fdm[prp.sim_time_s()], t_freeze, atol = 0.05) and fdm[prp.sim_time_s()] < 20):
                # ctx.freeze_actor(f16, lifetime = -1)
                t_freeze += 0.1
            i += 1

            f16_state = get_aircraft_state_from_fdm(fdm)
            
            f16_state.additional_data = {
                'Heading [deg]': round(fdm[prp.heading_deg()], 3)
            }

            aircrafts = {f16.name: f16_state}
            ctx.publish_simulation_state(
                SimulationState(
                    timestamp= round(fdm[prp.sim_time_s()], 2), 
                    aircrafts = aircrafts),
                time_sleep_s = 1e-5)
            
            