from __future__ import annotations
import zmq
import json
from collections import deque
from threading import Thread
import logging
import time
from typing import List, Union, Dict, NewType

from flypywire import SimulationState, AircraftState


LOGGING_FORMAT = '[%(asctime)s] %(message)s'
logging.basicConfig(format = LOGGING_FORMAT, level=logging.INFO)


class Publisher:

    def __init__(self,
        host: str = "tcp://127.0.0.1",
        port: int = 5555,
        debug: bool = False):
        
        self.host = host
        self.port = port
        self.address = f"{self.host}:{self.port}"

        self.debug = debug
        
        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.PUB)
        self.socket.bind(self.address)
        
    
    def __str__(self) -> str:

        return f'Publisher(address: {self.address})'
    
    def publish_simulation_state(self, state: SimulationState) -> None:

        self.socket.send_string(state.dumps())
        
        if self.debug: logging.info(msg = f'Publishing SimulationState:\n{state.dumps()}')

    def close(self) -> None:

        self.socket.close()
        logging.info(msg = f'Closing {self}')


class Subscriber:

    def __init__(self, 
        host: str = 'tcp://127.0.0.1',
        port: int = 5555,
        debug: bool = False,
        timeout_secs: float = 1):

        self.host = host
        self.port = port
        self.address = f'{self.host}:{self.port}'
        self.debug = debug
        self.timeout_secs = timeout_secs

        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.SUB)
        self.socket.connect(self.address)
        self.socket.subscribe("") #Subscribing to all topics in this address
        
        self.__last_msg_time = -10
        
        self._listener_thread = Thread(target = self._rcv_sim_state_str, daemon=True)

        self.buffer: deque[str] = deque(maxlen=10) #type: ignore

    def __str__(self) -> str:

        return f'Subscriber(address: {self.address})'
    
    @property
    def _timeout(self) -> bool:
        return time.time() - self.__last_msg_time > self.timeout_secs

    def _update_last_msg_time(self) -> None:
        self.__last_msg_time = time.time()
    

    def _rcv_sim_state_str(self) -> None:

        while True:
            try:
                msg = self.socket.recv_string(zmq.NOBLOCK)
                self.buffer.append(msg)
                self._update_last_msg_time()
                
                if self.debug: logging.info(msg = f'Receiving:\n{msg}')
            
            except zmq.error.Again:
                if self._timeout:
                    logging.info(msg = f'Waiting for connection...')
                    time.sleep(0.5)

        self.close()


    @property
    def is_data_available(self) -> bool:
        return len(self.buffer) > 0

    def start_listening(self) -> None:
        self._listener_thread.start()

    def get_simulation_state(self) -> SimulationState: # type: ignore
        return SimulationState.deserialize(self.buffer.pop())
        
        
    def close(self) -> None:
        self.socket.close()
        self._listener_thread.join()
        logging.info(msg = f'Closing {self}')