import json
from jsbsim import FGFDMExec
from flypywire.jsbsim_fdm import properties as prp

class AircraftState:


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
        
    def __str__(self) -> str:
        return "".join(["AircraftState:","\n", self.dumps()])
        
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

        return json.dumps(self.to_dict())


def get_aircraft_state_from_fdm(fdm: FGFDMExec) -> AircraftState:

        return AircraftState(
                fdm[prp.lat_geod_deg()],
                fdm[prp.lng_geoc_deg()],
                fdm[prp.altitude_sl_m()],
                fdm[prp.roll_rad()],
                fdm[prp.pitch_rad()],
                fdm[prp.yaw_rad()])