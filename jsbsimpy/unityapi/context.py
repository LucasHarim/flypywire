import time
from jsbsimpy.unityapi.game_services import GameServices
from jsbsimpy.unityapi.unityengine_classes import (
    Geolocation,
    Transform,
    Vector3,
    Color)

class SimulationContext:

    def __init__(self, client, cleanup_on_exit: bool = True):

        self.client = client
        self.cleanup_on_exit = cleanup_on_exit
        self.services = GameServices(self.client.socket)
        
        self.actor_clone_count = dict()

    def __enter__(self): 
        return self

    
    '''
        #TODO: Fixing problem with socket on exit.
        - The service self.destroy_all_actors() fails on exit if other services 
        are on going. It happens probably because the req-rep is not properly finished
    '''
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        
        if self.cleanup_on_exit: self.destroy_all_actors()


    # def list_assets(self) -> str:
    #     return self.services.list_assets("")
    
    def spawn_asset(self, game_asset: str, rolename: str, transform: Transform, parent_id: str = "") -> None:
        return self.services.spawn_asset(game_asset, rolename, transform.dumps(), parent_id)
    
    def destroy_actor(self, actor_id: str) -> None:
        return self.services.destroy_actor(actor_id)
    
    def destroy_all_actors(self) -> None:
        return self.services.destroy_all_actors()

    def get_transform(self, actor_id: str) -> Transform:
        return self.services.get_transform(actor_id)
    
    def set_transform(self, actor_id: str, transform: Transform) -> None:
        return self.services.set_transform(actor_id, transform.dumps())
    
    def get_position(self, actor_id) -> Vector3:
        return self.services.get_position(actor_id)
    
    def set_position(self, actor_id, position: Vector3) -> None:
        return self.services.set_position(actor_id, position.dumps())

    def get_geolocation(self, actor_id: str) -> Geolocation:
        return self.services.get_geolocation(actor_id)
    
    def set_geolocation(self, actor_id: str, geolocation: Geolocation) -> None:
        return self.services.set_geolocation(actor_id, geolocation.dumps())
    
    def freeze_actor(self, actor_id: str) -> None:

        if actor_id in self.actor_clone_count:
            self.actor_clone_count[actor_id] += 1
        else: 
            self.actor_clone_count[actor_id] = 1
        
        return self.services.freeze_actor(actor_id, f"{actor_id}.clone[{self.actor_clone_count.get(actor_id)}]")
    
    def draw_actor_trail(self, actor_id: str, width: float, start_color: Color = Color(1, 0, 0), end_color: Color = Color(0, 0, 1), lifetime: float = 10) -> None:
        
        label = f"{actor_id}.trajectory[{time.time_ns()}]"
        
        return self.services.draw_actor_trail(actor_id, width, start_color.dumps(), end_color.dumps(), label, lifetime)
    
    def draw_axis(self, transform: Transform, parent_id: str = "", size: float = 10) -> None:
        
        label = f"{parent_id}.axis.{time.time_ns()}"
        return self.services.draw_axis(transform.dumps(), parent_id, size, label)