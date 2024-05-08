import jsbsim
import numpy as np
from jsbsimpy import properties as prp
from jsbsimpy.fdm_pubsub import FDMPublisher

from pid import PIDController
from jsbsimpy.outputs import JFViewerOutputs

ROOT_DIR = '/home/lucas/jsbsim'
IC_PATH = 'examples/basic_ic.xml'
MODEL_NAME = 'A320'
SIM_DT = 0.033


fdm = jsbsim.FGFDMExec(root_dir = ROOT_DIR)
fdm.load_model(MODEL_NAME)
fdm.load_ic(IC_PATH, False)

fdm.set_dt(0.033)
fdm.run_ic()

pub = FDMPublisher(
    host = "tcp://127.0.0.1",
    port = 2000,
    topic = "topic/jsbsim", 
    time_sleep_s = 0.02,
    debug = True)

step = 0
fdm.run()


fdm[prp.gear_all_cmd.name] = 0
fdm[prp.throttle_cmd.name] = 0.75

catalog = fdm.query_property_catalog("propulsion")

dist_u_m = 0
aileron_control = PIDController(5, 0.0, 1.0, SIM_DT)
pitch_control = PIDController(0.5, 0.1, 0.2, SIM_DT)

while True:
    
    
    time = fdm[prp.sim_time_s.name]
    roll = np.pi/24 * np.sin(time)
    fdm[prp.aileron_cmd.name] = aileron_control.run_step(roll, fdm[prp.roll_rad.name])
    # fdm[prp.elevator_cmd.name] = pitch_control.run_step(0.0, fdm[prp.pitch_rad.name])
    
    # fdm[prp.elevator_cmd.name] = -0.08

    
    fdm.run()
    fdm_outputs = prp.get_outputs_from_fdm(fdm, JFViewerOutputs)
    pub.publish_fdm_outputs(fdm_outputs = {"step": step, **fdm_outputs}, realtime=True)

    step += 1 

    
    


