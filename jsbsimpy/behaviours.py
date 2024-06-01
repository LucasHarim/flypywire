from abc import ABC, abstractclassmethod
from py_trees.behaviour import Behaviour
from py_trees.common import Status
from typing import Union, Callable
import logging
from jsbsim import FGFDMExec

from jsbsimpy.properties import Property, BoundedProperty


class BaseBehaviour(Behaviour):

    def __init__(self, name: str) -> None:

        super().__init__(name)

    def initialise(self) -> None: ...

    def update(self) -> Status: ...
        
    def terminate(self, new_status: Status) -> None: ...


class WithinSimulationTimeRange(BaseBehaviour):

    def __init__(
        self,
        name: str,
        on_time_range_method: Callable[[None], None],
        fdm: FGFDMExec,
        t_end: float,
        t_init: float = 0,
        on_init: Callable[[None], None] = None,
        on_terminate: Callable[[None], None] = None) -> None:

        self.on_time_range_method = on_time_range_method
        self.fdm = fdm
        self.t_init = t_init
        self.t_end = t_end

        self.on_init = on_init
        self.on_terminate = on_terminate
        
        super().__init__(name)

        self._check_time_range()

    def _check_time_range(self) -> None:
        if self.t_init > self.t_end:

            raise ValueError(f'({self.t_init}, {self.t_end}) is not a valid time range. t_end must be greater than t_init.')
            
    def initialise(self) -> None:
        
        if self.on_init: self.on_init()

    def update(self) -> Status:

        if self.fdm.get_sim_time() < self.t_init: return Status.RUNNING

        elif (  self.fdm.get_sim_time() >= self.t_init\
            and self.fdm.get_sim_time() < self.t_end):
            
            self.on_time_range_method()
            return Status.RUNNING
        
        else: return Status.SUCCESS
    
    def terminate(self, new_status: Status) -> None:

        if self.on_terminate: self.on_terminate()



class SetFDMPropertyValue(BaseBehaviour):

    def __init__(
        self,
        name: str,
        fdm: FGFDMExec,
        property: Union[Property, BoundedProperty],
        value: Union[float, Callable[[None], float]],
        success_condition: Callable[[None], bool],
        on_init: Callable[[None], None] = None,
        on_terminate: Callable[[None], None] = None) -> None:

        self.fdm = fdm
        self.property = property
        self.value = value
        self.success_condition = success_condition
        self.on_init = on_init
        self.on_terminate = on_terminate

        super().__init__(name)

    def initialise(self) -> None:
        
        if self.on_init: self.on_init()

    def update(self) -> Status:
        
        _val = self.value
        if isinstance(self.value, Callable): _val = self.value()        
            
        self.fdm.set_property_value(self.property.name, _val)
        

        if self.success_condition(): return Status.SUCCESS

        return Status.RUNNING

    def terminate(self, new_status: Status) -> None:
        
        if self.on_terminate: self.on_terminate()

