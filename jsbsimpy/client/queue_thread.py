from __future__ import annotations
from queue import Queue
from threading import Thread
from typing import Callable, TypeVar, Tuple, List

T = TypeVar('T')

def _fill_queue_using_data_receiver(
        queue: Queue[T],
        rcv_data: Callable[[None], T]) -> None:
    while True:
        data = rcv_data()
        queue.put(data)

def make_queue_and_thread(
        rcv_data: Callable[[None], T],
        max_queue_size: int) -> Tuple[Queue[T], Thread]:
    
    queue: Queue[T] = Queue(max_queue_size)
    return queue, Thread(target = _fill_queue_using_data_receiver, args=(queue, rcv_data), daemon=True)


def on_queue_data(queue: Queue[T], func: Callable[[T], None]) -> None:

    while not queue.empty():
    
        func(queue.get_nowait())
        queue.task_done()

def create_test_data_generator(data: List[T]) -> Callable[[None], T]:
    data_iter = iter(data)

    return lambda: next(data_iter)