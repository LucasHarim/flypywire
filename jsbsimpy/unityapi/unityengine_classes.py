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
