from py_trees.behaviour import Behaviour
from py_trees.common import Status
from typing import Union, Callable, Optional
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
        timespan: Union[float, int, tuple, list],
        on_init: Callable[[None], None] = None,
        on_terminate: Callable[[None], None] = None) -> None:

        self.on_time_range_method = on_time_range_method
        self.fdm = fdm
        
        
        self.timespan = timespan
        self.t_init: Union[float, int] = None
        self.t_end: Union[float, int] = None

        if isinstance(self.timespan, (list, tuple)):
            self.t_init = self.timespan[0]
            self.t_end = self.timespan[1]

        self.on_init = on_init
        self.on_terminate = on_terminate
        
        super().__init__(name)
    
    def __str__(self) -> str:

        return f'[{self.name}] -> Timespan{self.t_init, self.t_end} | Duration({self.t_end - self.t_init}) '
    
    def _check_time_input(self) -> None:
        if self.t_init > self.t_end:

            raise ValueError(f'({self.t_init}, {self.t_end}) is not a valid time range. t_end must be greater than t_init.')
            
    def initialise(self) -> None:
        
        if isinstance(self.timespan, (float, int)): 
            self.t_init = self.fdm.get_sim_time()
            self.t_end = self.t_init + self.timespan
        
        self._check_time_input()

        if self.on_init: self.on_init()
        print(f'[Initializing]: {self}')

    def update(self) -> Status:

        if self.fdm.get_sim_time() < self.t_init: return Status.RUNNING

        elif (  self.fdm.get_sim_time() >= self.t_init\
            and self.fdm.get_sim_time() < self.t_end):
            
            self.on_time_range_method()
            return Status.RUNNING
        
        else: return Status.SUCCESS
    
    def terminate(self, new_status: Status) -> None:

        if self.on_terminate: self.on_terminate()
        print(f'[Terminating]: {self}')



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
        print(f'[Initializing]: {self.name}')

    def update(self) -> Status:
        
        _val = self.value
        if isinstance(self.value, Callable): _val = self.value()        
            
        self.fdm.set_property_value(self.property.name, _val)
        

        if self.success_condition(): return Status.SUCCESS

        return Status.RUNNING

    def terminate(self, new_status: Status) -> None:
        
        if self.on_terminate: self.on_terminate()
        print(f'[Terminating]: {self.name}')


class Trigger(BaseBehaviour):

    def __init__(
            self,
            name: str,
            success_condition: Callable[[None], bool],
            on_init: Callable[[None], None] = None,
            on_terminate: Callable[[None], None] = None) -> None:
        
        self.success_condition = success_condition
        self.on_init = on_init
        self.on_terminate = on_init
        super().__init__(name)

    
    def initialise(self) -> None:
        if self.on_init: self.on_init()
        print(f'[Initializing]: {self.name}')
    
    def update(self) -> Status:

        if self.success_condition(): return Status.SUCCESS

        return Status.RUNNING
    
    def on_terminate(self) -> None:

        if self.on_terminate: self.on_terminate()
        print(f'[Terminating]: {self.name}')