import json
from typing import Dict

from .aircraft_state import AircraftState

class SimulationFrame:

    def __init__(self, timestamp, aircrafts: Dict[str, AircraftState]):
        
        self.timestamp = timestamp
        self.aircrafts = aircrafts

    def dumps(self):

        sim_frame = {
            "Timestamp": self.timestamp,
            "Aircrafts": {
                aircraft: self.aircrafts[aircraft].to_dict() for aircraft in self.aircrafts
            }
        }
        
        return json.dumps(sim_frame)
