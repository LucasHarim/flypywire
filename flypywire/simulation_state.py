import json
from typing import Dict

from flypywire.aircraft_state import AircraftState

class SimulationState:

    def __init__(self, timestamp, aircrafts: Dict[str, AircraftState]):
        
        self.timestamp = timestamp
        self.aircrafts = aircrafts

    def __str__(self) -> str:
        return "".join(["SimulationState:", "\n", self.dumps()])
        
    def dumps(self) -> str:

        sim_state = {
            "Timestamp": self.timestamp,
            "Aircrafts": {
                aircraft: self.aircrafts[aircraft].to_dict() for aircraft in self.aircrafts
            }
        }
        
        return json.dumps(sim_state)
