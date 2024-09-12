
#! We get an error when import annotations!! It comes from service_request. Check how to solve it
# from __future__ import annotations 
import zmq
from zmq_requests import service_request
from flypywire import Publisher
from flypywire.unityapi.context import RenderContext
from flypywire.aircraft_state import AircraftState
from flypywire.unityapi.unityengine_classes import Transform, Vector3, Color


##TODO: Add a poller to Client in order to publish messages in a more controlled way. 
##TODO Get rid of time.sleep() for publishing in realtime
class Client:

    def __init__(self, host: str = 'tcp://127.0.0.1', port: int = 5555, timeout_ms: int = 5000, debug = False):

        self.host = host
        self.port = port
        self.req_port = port + 1
        self.debug = debug

        self.socket = zmq.Context().socket(zmq.REQ)
        self.socket.connect(f'{self.host}:{self.req_port}')
        self.socket.RCVTIMEO = timeout_ms

        self.publisher = Publisher(self.host, self.port, self.debug)

        self._check_connection_with_server()

        
    def RenderContext(self, cleanup_on_exit: bool = True) -> RenderContext:
        return RenderContext(self, cleanup_on_exit)


    @service_request
    def CheckClientConnection(self) -> None: ...

    def _check_connection_with_server(self) -> None:

        try: 
            self.CheckClientConnection()

        except zmq.error.Again:
            raise Exception(f'Timeout. Client cannot establish connection to server at {self.host}:{self.port}')
