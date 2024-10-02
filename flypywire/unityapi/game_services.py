import orjson
from zmq import Socket
from zmq_requests import service_request, Deserializers

from flypywire.unityapi.unityengine_classes import (
    Vector3,
    Transform,
    GeoCoordinate,
    Color)

def str_to_geocoordinate(val_str: str) -> GeoCoordinate:
    lon_lat_height = orjson.loads(val_str)
    return GeoCoordinate(lon_lat_height["Latitude"], lon_lat_height["Longitude"], lon_lat_height["Height"])

Deserializers.add_deserializer(Vector3, lambda val_str: Vector3(**orjson.loads(val_str)))
Deserializers.add_deserializer(GeoCoordinate, lambda val_str: str_to_geocoordinate(val_str))
Deserializers.add_deserializer(Transform, lambda val_str: Transform(Vector3(**orjson.loads(val_str)['position']), Vector3(**orjson.loads(val_str)['rotation'])))

class GameServices:

    def __init__(self, socket: Socket):

        self.socket = socket
    
    @service_request
    def GetAssetsLibrary(self) -> list: ...
    
    @service_request
    def SpawnGameObjectUsingGeoCoordinate(self, prefabName: str, roleName: str, geoCoordinate: str) -> None: ...

    @service_request
    def SpawnGameObjectAttachedToParent(self, prefabName: str, roleName: str, transform: str, parentName: str) -> None: ...
    
    @service_request
    def SpawnGameObjectRelativeToOther(self, prefabName: str, roleName: str, transform: str, otherName: str) -> None: ...

    @service_request
    def DestroyActor(self, actorName: str) -> None: ...

    @service_request
    def DestroyAllActors(self) -> None: ...

    @service_request
    def DestroyAllMarkers(self) -> None: ...

    @service_request
    def GetTransform(self, gameObjectName: str) -> Transform: ...

    @service_request
    def SetTransform(self, gameObjectName: str, transform: str) -> None: ...

    @service_request
    def GetPosition(self, gameObjectName: str, relativeTo: str) -> Vector3: ...

    @service_request
    def SetPosition(self, gameObjectName: str, position: str, relativeTo: str) -> None: ...

    @service_request
    def GetGeoCoordinate(self, gameObjectName: str) -> GeoCoordinate: ...

    @service_request
    def SetGeoCoordinate(self, gameObjectName: str, geoCoordinate: str) -> None: ...
        
    @service_request
    def FreezeActor(self, actorName: str, cloneName: str, lifetime: float) -> None: ...
    
    @service_request
    def SpawnCamera(self,
        label: str,
        parentName,
        transform: str,
        host: str,
        port: int,
        resolutionWidth: int,
        resolutionHeight: int) -> None: ...

    @service_request
    def DrawAxes(self,
        transform: str,
        width: float,
        size: float,
        label: str,
        parentName: str,
        lifetime: float,
        rightHand: bool) -> None: ...