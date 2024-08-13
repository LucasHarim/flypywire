from __future__ import annotations
import zmq
import json
from collections import deque
import jsbsim
from threading import Thread
from math import isnan
from typing import List, Union, Dict, NewType
import logging
import time

from jsbsimpy import properties as prp
from jsbsimpy.properties import Property, BoundedProperty


LOGGING_FORMAT = '[%(asctime)s] [%(topic)s] %(message)s'
logging.basicConfig(format = LOGGING_FORMAT, level=logging.INFO)

'''
    #TODO: 
    Make a function to send the information according to the following pattern example:

    {
        "timestamp": 1231213.312,
        "aircrafts": {
            "a320-main": {
                "latitude": -20.3102312312,
                "longitude": 5.123123123123,
                "altitude": 5012,
                "rollDeg": 0.0,
                "pitchDeg": 1.02,
                "yawDeg": -5.12
            },
            "a320-second": {
                "latitude": -20.3102312312,
                "longitude": 5.123123123123,
                "altitude": 5012,
                "rollDeg": 0.0,
                "pitchDeg": 1.02,
                "yawDeg": -5.12
            }
        }
    }

'''

def _is_topic_or_service_name_valid(topic: str) -> Union[None, bool]:
    
    not_allowed_names = ('topic/', 'service/')
    if topic.startswith(not_allowed_names): 
        raise NameError(f"{topic} is not a valid name. Please, remove {not_allowed_names}.")
    else: return True

def add_header_to_msg(header: str, data: str) -> str:

    return "".join([header, ":",data])

def add_timestamp(d: dict) -> dict:
    
    return {'timestamp': time.time(), **d}


PropertyName = NewType('PropertyName', str)
PropertyValue = NewType('PropertyValue', float)

class FDMPublisher:

    def __init__(self,
        host: str = "tcp://127.0.0.1",
        port: int = 5555,
        topic: str = "topic/jsbsim",
        time_sleep_s: float = 0.03,
        debug: bool = False):
        
        self.host = host
        self.port = port
        self.address = f"{self.host}:{self.port}"

        self.topic = topic
        self.time_sleep_s = time_sleep_s
        self.debug = debug
        
        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.PUB)
        self.socket.bind(self.address)
        
        self._selected_outputs = prp.DEFAULT_FDM_OUTPUTS
        self._step = 0
        
    
    def __str__(self) -> str:

        return f'FDMPublisher(address: {self.address}, topic: {self.topic})'
    
    def set_fdm_outputs(self,
        selected_outputs: List[Union[prp.Property, prp.BoundedProperty]]) -> None:
        
        self._selected_outputs = selected_outputs
    
    def _is_valid_fdm_output(self, output: float) -> bool:

        return not isnan(output)
        

    def publish_fdm_outputs(self,
        fdm_outputs: Dict[PropertyName, PropertyValue],
        realtime: bool = True) -> None:
        
        fdm_outputs = {'step': self._step, **fdm_outputs}
        _msg = add_header_to_msg(
                self.topic,
                json.dumps(add_timestamp(fdm_outputs)))
            
        if self._is_valid_fdm_output(fdm_outputs[prp.altitude_sl_ft.name]): 
            self.socket.send_string(_msg)
            self._step += 1

        else: 
            if self.debug: logging.warning(msg = f'A FDM output is NaN. Not publishing', extra = {'topic': self.topic})
        
        _msg_log = "".join([f'{name}: {value}\n' for name, value in list(fdm_outputs.items())])

        if self.debug: logging.info(msg = f'Sending message:\n{_msg_log}', extra = {'topic': self.topic})
        if realtime: time.sleep(self.time_sleep_s)

    def close(self) -> None:

        self.socket.close()
        logging.info(msg = f'Closing {self}', extra = {'topic': self.topic})

MsgType = NewType('MsgType', Union[str, dict])

class FDMSubscriber:

    def __init__(self, 
        host: str = 'tcp://127.0.0.1',
        port: int = 5555,
        topic: str = 'topic/jsbsim',
        debug: bool = False,
        timeout_secs: float = 1):

        self.host = host
        self.port = port
        self.address = f'{self.host}:{self.port}'
        self.topic = topic
        self.debug = debug
        self.timeout_secs = timeout_secs

        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.SUB)
        self.socket.connect(self.address)
        self.socket.subscribe(self.topic)
        
        self.__last_msg_time = -10
        
        self._listener_thread = Thread(target = self._rcv_fdm_outputs, daemon=True)

        self.buffer: deque[MsgType] = deque(maxlen=10) #type: ignore

    def __str__(self) -> str:

        return f'FDMSubscriber(address: {self.address}, topic: {self.topic})'
    
    @property
    def _timeout(self) -> bool:
        return time.time() - self.__last_msg_time > self.timeout_secs
    
    @property
    def is_data_available(self) -> bool:
        return len(self.buffer) > 0
    
    
    def _remove_topic_from_msg(self, msg: str) -> str:
        return msg.split(f"{self.topic}:")[-1]
    

    def _update_last_msg_time(self) -> None:
        self.__last_msg_time = time.time()
    

    def _rcv_fdm_outputs(self) -> None:
        
        while True:
            try:
                _raw_msg = self.socket.recv_string(zmq.NOBLOCK)
                self._update_last_msg_time()

                if self.debug: logging.info(msg = f'Receiving message:\n{_raw_msg}', extra = {'topic': self.topic})
            
                _msg = self._remove_topic_from_msg(_raw_msg)
                self.buffer.append(_msg)
        
            except zmq.error.Again:
                if self._timeout:
                    logging.info(msg = f'Waiting for connection...', extra = {'topic': self.topic})
                    time.sleep(0.5)
        
        self.close()


    def start_listening(self) -> None:
        self._listener_thread.start()


    def get_fdm_outputs(self, dtype: str | dict = dict) -> MsgType: # type: ignore
        
        try:    
            if dtype == dict: return json.loads(self.buffer.pop())
            return self.buffer.pop()
        
        except IndexError as e:            
            
            print('Trying to pop() from empty deque. Are you calling get_fdm_outputs() twice?')
        
        
    def close(self) -> None:
        self.socket.close()
        self._listener_thread.join()
        logging.info(msg = f'Closing {self}', extra = {'topic': self.topic})