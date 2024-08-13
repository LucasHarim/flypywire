import json
from typing import Dict
from dataclasses import dataclass

from .aircraft_state import AircraftState

@dataclass
class SimulationFrame:

    timestamp: float
    aircrafts: Dict[str, AircraftState]


    def dumps(self):

        sim_frame = {
            "Timestamp": self.timestamp,
            "Aircrafts": {
                aircraft: self.aircrafts[aircraft].to_dict() for aircraft in self.aircrafts
            }
        }
        
        return json.dumps(sim_frame)
