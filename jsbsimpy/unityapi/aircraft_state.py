import json
from dataclasses import dataclass

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
            'HeightMeters': self.height_m,
            'RollRad': self.roll_rad,
            "PitchRad": self.pitch_rad,
            "YawRad": self.yaw_rad}
        
    def dumps(self) -> str:

        return json.dumps(self.to_dict())
