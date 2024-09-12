from __future__ import annotations
import orjson
from typing import Dict, NewType
from flypywire.aircraft_state import AircraftState

AircraftName = NewType('AircraftName',str)

class SimulationState:

    def __init__(self, timestamp, aircrafts: Dict[AircraftName, AircraftState]):
        
        self.timestamp = timestamp
        self.aircrafts = aircrafts

    def __repr__(self) -> str:
        return "".join(["SimulationState:", "\n", self.dumps()])
    
    
    @staticmethod
    def deserialize(sim_state_str: str) -> SimulationState:

        sim_state_dict = orjson.loads(sim_state_str)
        aircrafts: Dict[str, dict] = sim_state_dict["Aircrafts"]
    
        for aircraft_name, aircraft_state_dict in aircrafts.items():
            aircrafts.update({aircraft_name: AircraftState.deserialize_dict(aircraft_state_dict)})
        
        return SimulationState(sim_state_dict["Timestamp"], aircrafts)
    
    def dumps(self) -> str:

        sim_state = {
            "Timestamp": self.timestamp,
            "Aircrafts": {
                aircraft_name: self.aircrafts[aircraft_name].to_dict() for aircraft_name in self.aircrafts.keys()
            }
        }
        
        return orjson.dumps(sim_state, option=orjson.OPT_INDENT_2).decode()
