import os
import jsbsim
from flypywire.jsbsim_fdm import properties as prp
import flypywire.unityapi as unity

def get_fdm(origin: unity.GeoCoordinate = unity.GeoCoordinate(-22.951804,  -43.210760, 2000), dt = 0.1):

    fdm = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT'))
    fdm.load_model('SGS')

    
    fdm[prp.initial_terrain_elevation_ft()] = 100
    fdm[prp.initial_u_fps()] = 100
    fdm[prp.initial_theta_deg()] = -1
    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * 3.3

    fdm.set_dt(dt)
    fdm.run_ic()

    return fdm
