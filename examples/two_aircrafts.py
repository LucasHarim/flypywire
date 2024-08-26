import os
import time
import jsbsim
from jsbsimpy import Client
from jsbsimpy.unityapi import (
    Transform,
    Vector3,
    GameObject,
    AircraftState, get_aircraft_state_from_fdm)

from jsbsimpy import properties as prp

if __name__ == '__main__':
    
    DT = 0.01
    
    fdm_a320 = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    fdm_a320.load_model('a320')
    
    fdm_a320.set_dt(DT)
    
    fdm_a320[prp.initial_latitude_geod_deg()] = 0.0
    fdm_a320[prp.initial_longitude_geoc_deg()] = 0.0
    fdm_a320[prp.initial_altitude_ft()] = 5000
    fdm_a320[prp.initial_u_fps()] = 1000

    fdm_a320.run_ic()

    client = Client()
    
    a320 = GameObject("Aircrafts/A320", 'main-a320')
    gripen = GameObject("Aircrafts/JAS39Gripen", 'gripen')
    
    with client.SimulationContext() as ctx:
        
        ctx.spawn_asset(a320)
        ctx.spawn_asset(gripen, Transform(Vector3(10, 10, 10), Vector3(0, 90, 0)))
        

        while True:
            
            fdm_a320.run()
            
            client.update_aircraft(a320.name, get_aircraft_state_from_fdm(fdm_a320))
            client.publish_aircraft_state()
            time.sleep(DT)
