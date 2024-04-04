import zmq
import json
import jsbsim
from math import isnan
from typing import List, Union, Dict, NewType
import logging
import time

from jsbsimpy import properties as prp
from jsbsimpy.properties import Property, BoundedProperty

LOGGING_FORMAT = '[%(asctime)s] [%(topic)s] %(message)s'
logging.basicConfig(format = LOGGING_FORMAT, level=logging.INFO)


def _is_topic_or_service_name_valid(topic: str) -> Union[None, bool]:
    
    not_allowed_names = ('topic/', 'service/')
    if topic.startswith(not_allowed_names): 
        raise NameError(f"{topic} is not a valid name. Please, remove {not_allowed_names}.")
    else: return True

def add_header_to_msg(header: str, data: str) -> str:

    return "".join([header, ":",data])

def add_timestamp(d: dict) -> dict:
    
    return {'timestamp': time.time(), **d}


DEFAULT_FDM_OUTPUTS = [
    prp.sim_time_s,
    prp.altitude_sl_ft,
    prp.lat_geod_deg,
    prp.lng_geoc_deg,
    prp.roll_rad,
    prp.pitch_rad,
    prp.heading_deg]

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
        
        self._selected_outputs = DEFAULT_FDM_OUTPUTS
        
    
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
        
        _msg = add_header_to_msg(
                self.topic,
                json.dumps(add_timestamp(fdm_outputs)))
            
        if self._is_valid_fdm_output(fdm_outputs[prp.altitude_sl_ft.valid_name]): 
            self.socket.send_string(_msg)

        else: 
            if self.debug: logging.warning(msg = f'A FDM output is NaN. Not publishing', extra = {'topic': self.topic})
        
        if self.debug: logging.info(msg = f'Sending message:\n{_msg}', extra = {'topic': self.topic})
        if realtime: time.sleep(self.time_sleep_s)

    def close(self) -> None:

        self.socket.close()
        logging.info(msg = f'Closing {self}', extra = {'topic': self.topic})


class FDMSubscriber:

    def __init__(self, host: str, port: int, topic: str, debug: bool = False):

        self.host = host
        self.port = port
        self.address = f'{self.host}:{self.port}'
        self.topic = topic
        self.debug = debug

        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.SUB)
        self.socket.connect(self.address)
        self.socket.subscribe(self.topic)

        self.__last_msg_time = -10
    
    def __str__(self) -> str:

        return f'FDMSubscriber(address: {self.address}, topic: {self.topic})'
    
    def _remove_topic_from_msg(self, msg: str) -> str:
        return msg.split(f"{self.topic}:")[-1]
    
    def _update_last_msg_time(self) -> None:
        self.__last_msg_time = time.time()
    
    def rcv_fdm_outputs(self, timeout : int = 1, output_dtype: Union[str, dict] = str) -> Union[str, dict]:
        
        ##TODO: make it an event driven function! 
        try: 
            _raw_msg = self.socket.recv_string(zmq.NOBLOCK)
            self._update_last_msg_time()

            if self.debug: logging.info(msg = f'Receiving message:\n{_raw_msg}', extra = {'topic': self.topic})
        
            _msg = self._remove_topic_from_msg(_raw_msg)

            if output_dtype == dict: return json.loads(_msg)
            else: return _msg
            
        except zmq.error.Again:
            
            if time.time() - self.__last_msg_time > timeout:
                logging.info(msg = f'Waiting for connection...', extra = {'topic': self.topic})
                time.sleep(0.5)
            

        
    
    def close(self) -> None:
        self.socket.close()
        logging.info(msg = f'Closing {self}', extra = {'topic': self.topic})