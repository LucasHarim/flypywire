from __future__ import annotations
from jsbsim import FGFDMExec
from .unityengine_classes import GameObject
from .aircraft_state import AircraftState
import jsbsimpy.properties as prp

class Actor(GameObject):

    def __init__(self, game_asset: str, parent: Actor, name: str = None) -> None:
        
        super().__init__(game_asset, name, parent)

    
    