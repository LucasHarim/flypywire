from jsbsimpy.unityapi.game_services import GameServices
from jsbsimpy.unityapi.unityengine_classes import (
    Geolocation,
    Vector3)

class SimulationContext:

    def __init__(self, client, cleanup_on_exit: bool = True):

        self.client = client
        self.cleanup_on_exit = cleanup_on_exit
        self.services = GameServices(self.client.socket)
    

    def __enter__(self): 
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        
        if self.cleanup_on_exit: self.destroy_all_actors()


    def list_assets(self) -> str:
        return self.services.list_assets()
    
    def spawn_asset(self, game_asset: str) -> None:
        return self.services.spawn_asset(game_asset)
    
    def destroy_actor(self, actor_id: str) -> None:
        return self.services.destroy_actor(actor_id)
    
    def destroy_all_actors(self) -> None:
        return self.services.destroy_all_actors()

    def get_position(self, actor_id) -> Vector3:
        return self.services.get_position(actor_id)
    
    def set_position(self, actor_id, position: Vector3) -> None:
        return self.services.set_position(actor_id, position.dumps())

    def get_geolocation(self, actor_id: str) -> Geolocation:
        return self.services.get_geolocation(actor_id)
    
    def set_geolocation(self, actor_id: str, geolocation: Geolocation) -> None:
        return self.services.set_geolocation(actor_id, geolocation.dumps())
    
    def freeze_actor(self, actor_id: str) -> None:
        return self.services.freeze_actor(actor_id)
    

    