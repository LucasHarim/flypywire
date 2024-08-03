import json
from zmq import Socket
from zmq_requests import service_request, Deserializers

from jsbsimpy.unityapi.unityengine_classes import (
    Vector3,
    Transform,
    Geolocation,
    Color)


Deserializers.add_deserializer(Vector3, lambda val_str: Vector3(**json.loads(val_str)))
Deserializers.add_deserializer(Geolocation, lambda val_str: Geolocation(**json.loads(val_str)))
Deserializers.add_deserializer(Transform, lambda val_str: Transform(Vector3(**json.loads(val_str)['position']), Vector3(**json.loads(val_str)['rotation'])))

class GameServices:

    def __init__(self, socket: Socket):

        self.socket = socket
    
    # @service_request
    # def list_assets(self, arg: str = "") -> str: ...

    @service_request
    def spawn_asset(self, game_asset: str, rolename: str, transform: str, parent_id: str = "") -> None: ...

    @service_request
    def destroy_actor(self, actor_id: str) -> None: ...

    @service_request
    def destroy_all_actors(self) -> None: ...

    @service_request
    def get_transform(self, actor_id: str) -> Transform: ...

    @service_request
    def set_transform(self, actor_id: str, transform: str) -> None: ...

    @service_request
    def get_position(self, actor_id: str) -> Vector3: ...

    @service_request
    def set_position(self, actor_id: str, position: str) -> None: ...

    @service_request
    def get_geolocation(self, actor_id: str) -> Geolocation: ...

    @service_request
    def set_geolocation(self, actor_id, geolocation: str) -> None: ...

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
    def draw_axis(self, transform: str, parent_id: str, size: float, label: str) -> None: ...