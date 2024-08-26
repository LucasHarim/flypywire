from __future__ import annotations
import json
from dataclasses import dataclass, asdict

class BaseDataclass:

    def dumps(self) -> str:

        return json.dumps(asdict(self))


@dataclass
class Vector3(BaseDataclass):

    x: float = 0
    y: float = 0
    z: float = 0

@dataclass
class Transform(BaseDataclass):

    position: Vector3 = Vector3()
    rotation: Vector3 = Vector3()

@dataclass
class Color(BaseDataclass):

    r: float = 1
    g: float = 1
    b: float = 1
    a: float = 1


@dataclass
class Geolocation(BaseDataclass):

    latitude: float
    longitude: float
    altitude: float


def context_required(function):
    
    def wrapper(function, *args, **kwargs):

        obj = args[0]
        if obj.context == None:
            raise Exception(f"Unable to call {function.__name__}. Context must be set first.")
        
        return function(*args, **kwargs)
    
    return wrapper


class GameObject:
    
    ITER = iter(range(1000))

    def __init__(self, game_asset: str, name: str, parent: GameObject = None, context = None):

        self.game_asset = game_asset
    
        if name == None:
            name = f"{game_asset}[{next(ITER)}]"
        
        self.name = name
        self.parent = parent

        self.context = context
    
    def set_context(self, context) -> None:
        self.context = context
    
    @context_required
    def spawn(self) -> None:
        self.context.spawn_gameobject(self)

    @context_required
    def get_position(self, relative_to: GameObject) -> Vector3:

        return self.context.get_position(self, relative_to)
    
    @context_required
    def set_position(self, position: Vector3, relative_to: GameObject) -> None:
        return self.context.set_position(self, position, relative_to) 
    