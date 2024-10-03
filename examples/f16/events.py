import numpy as np
from jsbsim import FGFDMExec

from py_trees.composites import Parallel, Sequence
from py_trees.common import ParallelPolicy
from py_trees.trees import BehaviourTree

from flypywire.jsbsim_fdm import properties as prp
from flypywire.jsbsim_fdm import behaviours as beh
from flypywire.control import PIDController
from flypywire import AircraftState

deg2rad = np.pi/180

def event_sequence(fdm: FGFDMExec, aircraft_state: AircraftState) -> BehaviourTree:
    
    pitch_controller = PIDController()
    roll_controller = PIDController()

    
    straight_flight = beh.WithinSimulationTimeRange(
        'Full Throttle and nose up',
        lambda: -pitch_controller.run_step(5*deg2rad, fdm[prp.pitch_rad()]),
        fdm,
        timespan = 5)
    
    turning = Parallel('Turning', ParallelPolicy.SUCCESS_ON_ALL, [
        
        beh.WithinSimulationTimeRange(
            'Aileron command',
            lambda: fdm.set_property_value(
                prp.aileron_cmd(),
                roll_controller.run_step(-60*deg2rad, fdm[prp.roll_rad()])),
            fdm,
            timespan = 600,
            on_terminate = lambda: fdm.set_property_value(prp.aileron_cmd(), 0.0)),
        
        beh.WithinSimulationTimeRange(
            'Elevator command',
            lambda: fdm.set_property_value(
                prp.elevator_cmd(),
                -pitch_controller.run_step(10*deg2rad, fdm[prp.pitch_rad()])),
            fdm,
            timespan = 600,
            on_terminate = lambda: fdm.set_property_value(prp.elevator_cmd(), 0.0))
        ])
    
    
    
    root = Sequence('main-sequence', [
        straight_flight,
        turning,
        beh.Idle(fdm)
    ])

    
    return BehaviourTree(root)
