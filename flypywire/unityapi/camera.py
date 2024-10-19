import numpy as np
import zmq
import cv2
import time
from queue import Queue
from typing import Callable
from threading import Thread

class Camera:

    def __init__(self, host: str = 'tcp://127.0.0.1', port: int = 2000):
        
        self.host = host
        self.port = port

        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect(f'{self.host}:{self.port}')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.queue: Queue[np.array] = Queue(10)
        self.thread = Thread(target = self._enqueue_imgs, daemon=True)
        
        self.thread.start()
        self._close_window = False
    
    @property
    def img_available(self) -> bool:
        return not self.queue.empty()
    
    def _enqueue_imgs(self) -> None:

        while True:

            arr = np.frombuffer(self.socket.recv(), dtype = np.uint8)
            
            if self.queue.full():
                _ = self.queue.get_nowait()
                self.queue.task_done()
            
            self.queue.put(cv2.imdecode(arr, flags = cv2.IMREAD_COLOR))
    
    def get_image(self) -> np.array:
        
        img = self.queue.get_nowait()
        self.queue.task_done()
        return img


    def imshow(self, winname: str = 'Camera') -> np.array:
        
        if self.img_available:
            if not self._close_window:
                frame = self.get_image()
                cv2.imshow(winname, frame)
            
            if cv2.waitKey(1) == ord('q'):
                self._close_window = True
                cv2.destroyWindow(winname)
            
            return frame

if __name__ == '__main__':

    cam = Camera(port = 2000)
        
    while True:
        
        cam.imshow()

