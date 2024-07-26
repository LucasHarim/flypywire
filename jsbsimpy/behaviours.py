from py_trees.behaviour import Behaviour
from py_trees.common import Status
from py_trees.composites import Sequence
from typing import Union, Callable, Optional
import logging
from numpy import round
from jsbsim import FGFDMExec

import jsbsimpy.properties as prp
from jsbsimpy.properties import Property, BoundedProperty
from jsbsimpy.control import PIDController

INF = 10**9

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

        return f'[{self.name}] -> Timespan{round(self.t_init, 3), round(self.t_end, 3)} | Duration({self.t_end - self.t_init}) '
    
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
    
    def terminate(self) -> None:

        if self.on_terminate: self.on_terminate()
        print(f'[Terminating]: {self.name}')


class StallTrigger(Trigger):

    def __init__(self, name: str, fdm: FGFDMExec, on_init: Callable = None, on_terminate: Callable = None):
        
        self.fdm = fdm
        super().__init__(name, success_condition = lambda: self.check_stall(), on_init=on_init, on_terminate=on_terminate)
    
    def check_stall(self) -> bool:
        return self.fdm[prp.v_down_fps()] >= 0 and self.fdm[prp.pitch_rad()] <= 0


def Idle(fdm: FGFDMExec, timespan: float = INF) -> WithinSimulationTimeRange:

    return WithinSimulationTimeRange(
            f'Holding for {timespan} seconds',
            lambda: None,
            fdm,
            timespan= timespan)

class CmdDoublet(BaseBehaviour):

    def __init__(self, name, fdm: FGFDMExec, fcs_target: Property | BoundedProperty,
                amplitude_norm: float = 1, period: float = 1, on_init: callable = None, on_terminate: callable = None):

        super().__init__(name)
        self.fcs_target = fcs_target
        self.fdm = fdm
        self.amplitude = amplitude_norm
        self.period = period
        self.on_init = on_init
        self.on_terminate = on_terminate

        
        self.positive_cmd = WithinSimulationTimeRange(
            f'{name} - positive cmd',
            fdm = fdm,
            on_time_range_method=  lambda: self.fdm.set_property_value(self.fcs_target.name, self.amplitude),
            timespan=self.period/2)
        
        self.negative_cmd = WithinSimulationTimeRange(
            f'{name} - negative cmd',
            fdm = fdm,
            on_time_range_method = lambda: self.fdm.set_property_value(self.fcs_target.name, -self.amplitude),
            timespan= self.period/2,
            on_terminate= lambda: self.fdm.set_property_value(self.fcs_target.name, 0))
        
        self.cmd_seq = Sequence(self.name, [self.positive_cmd, self.negative_cmd])
    

    def initialise(self) -> None:
        
        if self.on_init: self.on_init()
        print(f'[Initializing]: {self.name}')

    def update(self) -> Status:
        
        
        [item.update() for item in self.cmd_seq.tick()]
        
        if self.cmd_seq.children[-1].status == Status.SUCCESS: 
            return Status.SUCCESS
            
        return Status.RUNNING
    
    
    def terminate(self, new_status: Status) -> None:
        
        if self.on_terminate: self.on_terminate()
        
        print(f'[Terminating]: {self.name}')
        

        
    


