import json
from zmq import Socket
from zmq_requests import service_request, Deserializers

from jsbsimpy.unityapi.unityengine_classes import (
    Vector3,
    Geolocation)


Deserializers.add_deserializer(Vector3, lambda val_str: Vector3(**json.loads(val_str)))
Deserializers.add_deserializer(Geolocation, lambda val_str: Geolocation(**json.loads(val_str)))

class GameServices:

    def __init__(self, socket: Socket):

        self.socket = socket
    
    @service_request
    def list_assets(self) -> str: ...

    @service_request
    def spawn_asset(self, game_asset: str) -> None: ...

    @service_request
    def destroy_actor(self, actor_id: str) -> None: ...

    @service_request
    def destroy_all_actors(self) -> None: ...

    @service_request
    def get_position(self, actor_id: str) -> Vector3: ...

    @service_request
    def set_position(self, actor_id: str, position: str) -> None: ...

    @service_request
    def get_geolocation(self, actor_id: str) -> Geolocation: ...

    @service_request
    def set_geolocation(self, actor_id, geolocation: str) -> None: ...

    @service_request
    def freeze_actor(self, actor_id: str) -> None: ...
