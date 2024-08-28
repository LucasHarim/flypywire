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
    height_m: float

    
    def dumps(self) -> str:
        data = {
            "Longitude": self.longitude,
            "Latitude": self.latitude,
            "Height": self.height_m
        }
        
        return json.dumps(data)
    
def context_required(function):
    
    def wrapper(function, *args, **kwargs):

        obj = args[0]
        if obj.context == None:
            raise Exception(f"Unable to call {function.__name__}. Context must be set first.")
        
        return function(*args, **kwargs)
    
    return wrapper


class GameObject:

    def __init__(self, name: str, prefab: str):

        self.name = name
        self.prefab = prefab
        