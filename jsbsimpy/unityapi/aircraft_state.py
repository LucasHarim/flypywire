import json
from dataclasses import dataclass
from jsbsim import FGFDMExec
import jsbsimpy.properties as prp

@dataclass
class AircraftState:

    latitude: float
    longitude: float
    height_m: float
    roll_rad: float = 0
    pitch_rad: float = 0
    yaw_rad: float = 0

    def to_dict(self) -> dict:
        return {
            'Latitude': self.latitude,
            'Longitude': self.longitude,
            'AltitudeMeters': self.height_m,
            'RollRad': self.roll_rad,
            "PitchRad": self.pitch_rad,
            "YawRad": self.yaw_rad
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