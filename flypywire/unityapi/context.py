import time
from flypywire import SimulationState
from flypywire.unityapi.game_services import GameServices
from flypywire.unityapi import (
    Geolocation,
    Transform,
    Vector3,
    GameObject,
    Color)


class RenderContext:

    def __init__(self, client, cleanup_on_exit: bool = True):

        self.client = client
        self.publisher = self.client.publisher
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
        
        if self.cleanup_on_exit: 
            self.destroy_all_actors()
            self.destroy_all_markers()

    def publish_simulation_state(self,
        simulation_state: SimulationState,
        time_sleep_s: float = 0.03) -> None:
        
        self.publisher.publish_simulation_state(simulation_state)
        time.sleep(time_sleep_s)

    
    def get_prefab_library(self) -> str:
        return self.services.get_prefab_library()
    
    def spawn_gameobject(
            self,
            gameobject: GameObject,
            transform: Transform = Transform(),
            geolocation: Geolocation = None,
            relative_to: GameObject = None,
            attach: bool = False) -> None: ##TODO: make this function return an Actor
        
        if geolocation:
            return self.services.spawn_gameobject_using_geolocation(
                gameobject.prefab,
                gameobject.name,
                geolocation.dumps())
        
        elif attach: 
            return self.services.spawn_gameobject_attached_to_parent(
                gameobject.prefab,
                gameobject.name,
                transform.dumps(),
                relative_to.name)
        
        elif relative_to:
            return self.services.spawn_gameobject_relative_to_other(
                gameobject.prefab,
                gameobject.name,
                transform.dumps(),
                relative_to.name)
        
        return self.services.spawn_gameobject_using_transform(
            gameobject.prefab,
            gameobject.name,
            transform.dumps())
            

    def spawn_asset(self, game_asset: str, rolename: str, transform: Transform, parent_id: str = "") -> None:
        return self.services.spawn_asset(game_asset, rolename, transform.dumps(), parent_id)
    
    def destroy_actor(self, actor_id: str) -> None:
        return self.services.destroy_actor(actor_id)
    
    def destroy_all_actors(self) -> None:
        return self.services.destroy_all_actors()
    
    def destroy_all_markers(self) -> None:
        return self.services.destroy_all_markers()

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
    
    def get_origin(self) -> Geolocation:
        return self.get_geolocation("SimulationOrigin")
    
    def set_origin(self, geolocation: Geolocation) -> None:
        return self.set_geolocation("SimulationOrigin", geolocation)
    
    def freeze_actor(self, actor_id: str) -> None:

        if actor_id in self.actor_clone_count:
            self.actor_clone_count[actor_id] += 1
        else: 
            self.actor_clone_count[actor_id] = 1
        
        return self.services.freeze_actor(actor_id, f"{actor_id}.clone[{self.actor_clone_count.get(actor_id)}]")
    
    def draw_actor_trail(self, actor_id: str, width: float, start_color: Color = Color(1, 0, 0), end_color: Color = Color(0, 0, 1), lifetime: float = 10) -> None:
        
        label = f"{actor_id}.trajectory[{time.time_ns()}]"
        
        return self.services.draw_actor_trail(actor_id, width, start_color.dumps(), end_color.dumps(), label, lifetime)
    
    def draw_axes(self, 
        width: float = 0.01,
        size: float = 1,
        transform: Transform = Transform(),
        parent_id: str = "",
        lifetime: float = -1,
        right_hand: bool = False) -> None:
        
        label = f"{parent_id}.axes.{time.time_ns()}"
        return self.services.draw_axes(transform.dumps(), width, size, label, parent_id, lifetime, right_hand)