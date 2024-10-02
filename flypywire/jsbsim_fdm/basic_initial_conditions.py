import os
import jsbsim
from flypywire.jsbsim_fdm import properties as prp
from flypywire.unityapi import GeoCoordinate

m2ft = 3.281

cruise_speed_fts = {
    "f22": 1790,
    "f16": 846,
    "B747": 850,
    '787-8': 874,
    "A320": 765.5,
    "SGS": 77.7,
    "F450": 0.0,
    "T38": 513,
    "c172p": 206,
    't6texan2': 469,
    'J3Cub': 110
}

def setup_cruise_condition(model: str, origin: GeoCoordinate) -> jsbsim.FGFDMExec:
    
    fdm = jsbsim.FGFDMExec(os.getenv('JSBSIM_ROOT')) 
    fdm.load_model(model)

    fdm[prp.initial_latitude_geod_deg()] = origin.latitude
    fdm[prp.initial_longitude_geoc_deg()] = origin.longitude
    fdm[prp.initial_altitude_ft()] = origin.height_m * m2ft
    fdm[prp.initial_u_fps()] = cruise_speed_fts[model]
    fdm[prp.engine_running()] = 1
    fdm[prp.gear()] = 0
    fdm[prp.gear_all_cmd()] = 0.0 ## Landing Gears Up

    fdm.run_ic()

    return fdm