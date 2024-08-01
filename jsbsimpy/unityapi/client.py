
#! We get an error when import annotations!! It comes from service_request. Check how to solve it
# from __future__ import annotations 
import zmq
from typing import List
from jsbsimpy.unityapi.context import SimulationContext

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

    
    
