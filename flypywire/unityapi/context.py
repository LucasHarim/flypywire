import time
from typing import Union
from flypywire import SimulationState
from flypywire.unityapi.game_services import GameServices
from flypywire.unityapi import (
    GeoCoordinate,
    Transform,
    Vector3,
    GameObject,
    Actor)

from flypywire.unityapi.camera import Camera


SimulationOrigin = GameObject('SimulationOrigin', None)

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
        if time_sleep_s > 0: time.sleep(time_sleep_s)

    
    def get_assets_library(self) -> str:
        return self.services.GetAssetsLibrary()
    
    def spawn_actor(self, actor: Actor, coordinate: GeoCoordinate) -> None:

        return self.services.SpawnGameObjectUsingGeoCoordinate(actor.asset_path, actor.rolename, coordinate.dumps())
    
    def spawn_gameobject(
            self,
            gameobject: GameObject,
            transform: Transform = Transform(),
            geocoordinate: GeoCoordinate = None,
            relative_to: GameObject = SimulationOrigin,
            attach: bool = False) -> None: ##TODO: make this function return an Actor
        
        if geocoordinate:
            return self.services.SpawnGameObjectUsingGeoCoordinate(
                gameobject.prefab,
                gameobject.name,
                geocoordinate.dumps())
        
        elif attach: 
            return self.services.SpawnGameObjectAttachedToParent(
                gameobject.prefab,
                gameobject.name,
                transform.dumps(),
                relative_to.name)
        
        else:
            return self.services.SpawnGameObjectRelativeToOther(
                gameobject.prefab,
                gameobject.name,
                transform.dumps(),
                relative_to.name)
    
    def destroy_actor(self, actor: Union[Actor,GameObject]) -> None:
        return self.services.DestroyActor(actor.name)
    
    def destroy_all_actors(self) -> None:
        return self.services.DestroyAllActors()
    
    def destroy_all_markers(self) -> None:
        return self.services.DestroyAllMarkers()

    def get_transform(self, actor: Union[Actor,GameObject]) -> Transform:
        return self.services.GetTransform(actor.name)
    
    def set_transform(self, actor: Union[Actor,GameObject], transform: Transform) -> None:
        return self.services.SetTransform(actor.name, transform.dumps())
    
    def get_position(self, actor: Union[Actor,GameObject], relative_to: GameObject = SimulationOrigin) -> Vector3:
        return self.services.GetPosition(actor.name, relative_to.name)
    
    def set_position(self, actor: Union[Actor,GameObject], position: Vector3, relative_to: GameObject = SimulationOrigin) -> None:
        return self.services.SetPosition(actor.name, position.dumps(), relative_to.name)

    def get_geocoordinate(self, actor: GameObject) -> GeoCoordinate:
        return self.services.GetGeoCoordinate(actor.name)
    
    def set_geocoordinate(self, actor: GameObject, geocoordinate: GeoCoordinate) -> None:
        return self.services.SetGeoCoordinateUsingStrings(actor.name, geocoordinate.dumps())
    
    def get_origin(self) -> GeoCoordinate:
        return self.get_geocoordinate(SimulationOrigin)
    
    def set_origin(self, geocoordinate: GeoCoordinate) -> None:
        return self.set_geocoordinate(SimulationOrigin, geocoordinate)
    
    def freeze_actor(self, actor: Union[Actor,GameObject], lifetime: float = -1) -> None:

        if actor.name in self.actor_clone_count:
            self.actor_clone_count[actor.name] += 1
        else: 
            self.actor_clone_count[actor.name] = 1
        clone_name = f"{actor.name}.clone[{self.actor_clone_count.get(actor.name)}]"
        return self.services.FreezeActor(actor.name, clone_name, lifetime)
    
    def spawn_camera(self,
        label: str,
        parent: Union[Actor,GameObject],
        transform: Transform = Transform(),
        host: str = 'tcp://127.0.0.1',
        port: int = 2000,
        resolution_width: int = 640,
        resolution_height: int = 480) -> Camera:
        
        self.services.SpawnCamera(
            label, parent.name,
            transform.dumps(),
            host, port,
            resolution_width,
            resolution_height)
        
        return Camera(host, port)
    
    def draw_axes(self, 
        width: float = 0.01,
        size: float = 1,
        transform: Transform = Transform(),
        parent: Union[Actor,GameObject] = SimulationOrigin,
        lifetime: float = -1,
        right_hand: bool = False) -> GameObject:
        
        label = f"{parent.name}.axes.{time.time_ns()}"
        
        self.services.DrawAxes(
            transform.dumps(),
            width, size, label,
            parent.name,
            lifetime,
            right_hand)
        
        axes = GameObject(label, None)
        
        return axes

        