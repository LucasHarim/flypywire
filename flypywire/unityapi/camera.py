import numpy as np
import zmq
import cv2
import time
from queue import Queue
from threading import Thread

class Camera:

    def __init__(self, host: str = 'tcp://127.0.0.1', port: int = 2000):
        
        self.host = host
        self.port = port

        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect(f'{self.host}:{self.port}')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.queue: Queue[np.array] = Queue(10)
    
    @property
    def is_connected(self) -> bool:
        return self.socket.poll(timeout = 100, flags=zmq.POLLIN)
    
    def get_image(self):
        
        arr = np.frombuffer(self.socket.recv(), dtype = np.uint8)
        return cv2.imdecode(arr, flags = cv2.IMREAD_COLOR)

if __name__ == '__main__':

    cam = Camera(port = 2000)
        
    while True:
        
        if cam.is_connected:
            frame = cam.get_image()
            cv2.imshow('Camera', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
    cv2.destroyAllWindows()

