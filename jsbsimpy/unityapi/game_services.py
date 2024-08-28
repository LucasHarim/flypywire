import json
from zmq import Socket
from zmq_requests import service_request, Deserializers

from jsbsimpy.unityapi.unityengine_classes import (
    Vector3,
    Transform,
    Geolocation,
    Color)

def str_to_geolocation(val_str: str) -> Geolocation:
    lon_lat_height = json.loads(val_str)
    return Geolocation(lon_lat_height["Latitude"], lon_lat_height["Longitude"], lon_lat_height["Height"])

Deserializers.add_deserializer(Vector3, lambda val_str: Vector3(**json.loads(val_str)))
Deserializers.add_deserializer(Geolocation, lambda val_str: str_to_geolocation(val_str))
Deserializers.add_deserializer(Transform, lambda val_str: Transform(Vector3(**json.loads(val_str)['position']), Vector3(**json.loads(val_str)['rotation'])))

class GameServices:

    def __init__(self, socket: Socket):

        self.socket = socket
    
    @service_request
    def get_assets_library(self) -> list: ...
    
    @service_request
    def spawn_gameobject_using_geolocation(self, prefab: str, name: str, geolocation: str) -> None: ...

    @service_request
    def spawn_gameobject_attached_to_parent(self, prefab: str, name: str, transform: str, parent_name: str) -> None: ...
    
    @service_request
    def spawn_gameobject_relative_to_other(self, prefab: str, name: str, transform: str, other_name: str) -> None: ...

    @service_request
    def spawn_gameobject_using_transform(self, prefab: str, name: str, transform: str) -> None: ...

    @service_request
    def spawn_asset(self, game_asset: str, rolename: str, transform: str, parent_id: str = "") -> None: ...

    @service_request
    def destroy_actor(self, actor_id: str) -> None: ...

    @service_request
    def destroy_all_actors(self) -> None: ...

    @service_request
    def destroy_all_markers(self) -> None: ...

    @service_request
    def get_transform(self, actor_id: str) -> Transform: ...

    @service_request
    def set_transform(self, actor_id: str, transform: str) -> None: ...

    @service_request
    def get_position(self, actor_id: str) -> Vector3: ...

    @service_request
    def set_position(self, actor_id: str, position: str) -> None: ...

    @service_request
    def get_geolocation(self, gameObjectName: str) -> Geolocation: ...

    @service_request
    def set_geolocation(self, gameObjectName, geolocation: str) -> None: ...
        
    @service_request
    def freeze_actor(self, actor_id: str, clone_name: str) -> None: ...

    @service_request
    def draw_actor_trail(self,
        actor_id: str,
        width: float,
        start_color: Color,
        end_color: Color,
        label: str,
        lifetime: float) -> None: ...

    @service_request
    def draw_axes(self,
        transform: Transform,
        width: float,
        size: float,
        label: str,
        parent_id: str,
        lifetime: float,
        right_hand: bool) -> None: ...