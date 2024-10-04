from __future__ import annotations
import orjson
from typing import Dict, NewType
from flypywire.actor_state import ActorState

ActorName = NewType('ActorName',str)

class SimulationState:

    def __init__(self, timestamp, actors: Dict[ActorName, ActorState]):
        
        self.timestamp = timestamp
        self.actors = actors

    def __repr__(self) -> str:
        return "".join(["SimulationState:", "\n", self.dumps()])
    
    
    @staticmethod
    def deserialize(sim_state_str: str) -> SimulationState:

        sim_state_dict = orjson.loads(sim_state_str)
        actors: Dict[str, dict] = sim_state_dict["Actors"]
    
        for actor_name, actor_state_dict in actors.items():
            actors.update({actor_name: ActorState.deserialize_dict(actor_state_dict)})
        
        return SimulationState(sim_state_dict["Timestamp"], actors)
    
    def dumps(self) -> str:

        sim_state = {
            "Timestamp": self.timestamp,
            "Actors": {
                actor_name: self.actors[actor_name].to_dict() for actor_name in self.actors.keys()
            }
        }
        
        return orjson.dumps(sim_state, option=orjson.OPT_INDENT_2).decode()
