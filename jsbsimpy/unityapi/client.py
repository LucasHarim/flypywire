
#! We get an error when import annotations!! It comes from service_request. Check how to solve it
# from __future__ import annotations 
import zmq
import json
from typing import List
from zmq_requests import service_request
from jsbsimpy.unityapi.context import SimulationContext
from jsbsimpy.unityapi.unityengine_classes import Transform, Vector3, Color
import time
import numpy as np
class Client:

    def __init__(self, host: str = 'tcp://127.0.0.1', port: int = 5555, timeout_ms: int = 5000):

        self.host = host
        self.port = port
        self.socket = zmq.Context().socket(zmq.REQ)
        self.socket.connect(f'{host}:{port}')
        self.socket.RCVTIMEO = timeout_ms

        self._check_connection_with_server()

        
    def SimulationContext(self, cleanup_on_exit: bool = True) -> SimulationContext:
        return SimulationContext(self, cleanup_on_exit)


    @service_request
    def CheckClientConnection(self) -> None: ...

    def _check_connection_with_server(self) -> None:

        try: 
            self.CheckClientConnection()

        except zmq.error.Again:
            raise Exception(f'Timeout. Client cannot establish connection to server at {self.host}:{self.port}')

    
    
if __name__ == '__main__':

    client = Client()
    connected = True

    u = 0.5
    t = 0

    with client.SimulationContext() as ctx:
        
        ctx.destroy_all_actors()
        ctx.spawn_asset(
            game_asset="Aircrafts/Missile",
            rolename='Main-Missile',
            transform= Transform(Vector3(10, 10, 10), Vector3(0, 0, -90)))
        
        ctx.spawn_asset(
            game_asset="Aircrafts/Missile",
            rolename='Side-Missile',
            transform= Transform(Vector3(5, 5, 5), Vector3(0, 0, 90)),
            parent_id='Main-Missile')

        ctx.draw_actor_trail("Main-Missile", width = 0.1, start_color = Color(1, 1, 0), end_color=Color(0, 1, 0),lifetime = 10)
        ctx.draw_axis(Transform(), "Main-Missile")

        while connected:
            
            pos = Vector3(u * t, 2*np.sin(t), 2*np.cos(t))
            rot = Vector3(30*np.sin(0.1*t), 30*np.cos(0.1*t), 45*np.sin(0.05*t))

            ctx.set_transform('Main-Missile', Transform(pos,rot))
            # ctx.set_position('Main-Missile', pos)
            
            if t%5 == 0: ctx.freeze_actor('Main-Missile')

            t += 1

            if t > 100: break

        
        time.sleep(100)

        