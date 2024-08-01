import json
from dataclasses import dataclass, asdict

class BaseDataclass:

    def dumps(self) -> str:

        return json.dumps(asdict(self))


@dataclass
class Vector3(BaseDataclass):

    x: float
    y: float
    z: float

    def __init__(self, x = 0, y = 0, z = 0):
        
        self.x = x
        self.y = y
        self.z = z


@dataclass
class Transform(BaseDataclass):

    position: Vector3
    rotation: Vector3

    def __init__(self, position = Vector3(), rotation = Vector3()):

        self.position = position
        self.rotation = rotation


@dataclass
class Color(BaseDataclass):

    r: float
    g: float
    b: float
    a: float


@dataclass
class Geolocation(BaseDataclass):

    latitude: float
    longitude: float
    altitude: float
