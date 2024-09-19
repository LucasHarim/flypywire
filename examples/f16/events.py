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

    landing_gear_up_trigger = beh.Trigger(
        'LG-Up trigger',
        on_init= lambda: aircraft_state.additional_data.update({'Event': 'LG-Up'}) ,
        success_condition = lambda: not bool(fdm[prp.gear()]))
    
    wait_2s = beh.Idle(
        fdm,
        timespan=2)
    
    nose_up_until_stall = Parallel('Inducing Stall', ParallelPolicy.SUCCESS_ON_ALL,
    [
        beh.WithinSimulationTimeRange(
            'Pitch-Up',
            lambda: fdm.set_property_value(
                prp.elevator_cmd(),
                -pitch_controller.run_step(
                    60 * deg2rad,
                    fdm[prp.pitch_rad()]
                )
            ),
            fdm,
            timespan = 1000),
        
        beh.StallTrigger(
            'Stall-Trigger',
            fdm,
            on_terminate= lambda: fdm.set_property_value(prp.elevator_cmd(), 0))    
    ])

    
    
    root = Sequence('main-sequence', [
        landing_gear_up_trigger,
        wait_2s,
        nose_up_until_stall,
        beh.Idle(fdm)
    ])

    
    return BehaviourTree(root)
