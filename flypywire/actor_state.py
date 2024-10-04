from __future__ import annotations
import orjson
from math import isnan
from jsbsim import FGFDMExec
from flypywire.jsbsim_fdm import properties as prp

class ActorState:

    def __init__(self,
        latitude: float,
        longitude: float,
        height_m: float,
        roll_rad: float,
        pitch_rad: float,
        yaw_rad: float,
        **additional_data):

        self.latitude = latitude
        self.longitude = longitude
        self.height_m = height_m
        self.roll_rad = roll_rad
        self.pitch_rad = pitch_rad
        self.yaw_rad = yaw_rad
        self.additional_data = additional_data
        
    def __repr__(self) -> str:
        return "".join(["ActorState:","\n", self.dumps()])

    @staticmethod
    def deserialize_dict(actor_state_dict: dict) -> ActorState:
        
        actor_state = ActorState(
            actor_state_dict["Latitude"],
            actor_state_dict["Longitude"],
            actor_state_dict["AltitudeMeters"],
            actor_state_dict["RollRad"],
            actor_state_dict["PitchRad"],
            actor_state_dict["YawRad"])
        
        actor_state.additional_data = dict([(key, actor_state_dict[key])\
            for key in list(actor_state_dict.keys())[6:]])
        
        return actor_state


    def to_dict(self) -> dict:
        return {
            'Latitude': self.latitude,
            'Longitude': self.longitude,
            'AltitudeMeters': self.height_m,
            'RollRad': self.roll_rad,
            "PitchRad": self.pitch_rad,
            "YawRad": self.yaw_rad,
            **self.additional_data
        }        
        

    def dumps(self) -> str:
        return orjson.dumps(self.to_dict(), option=orjson.OPT_INDENT_2).decode("utf-8")


def get_aircraft_state_from_fdm(fdm: FGFDMExec, terrain_elevation_m: float = 0) -> ActorState:
        
        values = (
            fdm[prp.lat_geod_deg()],
            fdm[prp.lng_geoc_deg()],
            fdm[prp.altitude_sl_m()] - terrain_elevation_m,
            fdm[prp.roll_rad()],
            fdm[prp.pitch_rad()],
            fdm[prp.yaw_rad()])
        
        for v in values:
            if isnan(v):
                raise Exception("FDM output is not a number.")
                return None
            
        return ActorState(*values)
        