import jsbsim
import numpy as np
from jsbsimpy import properties as prp
from jsbsimpy.fdm_pubsub import FDMPublisher
from pid import PIDController

from pid import PIDController
from jsbsimpy.outputs import JFViewerOutputs

ROOT_DIR = '/home/lucas/jsbsim'
IC_PATH = 'examples/basic_ic.xml'
MODEL_NAME = 'A320'
SIM_DT = 0.03
DEG_TO_RAD = np.pi / 180
FT_TO_M = 0.3048

fdm = jsbsim.FGFDMExec(root_dir = ROOT_DIR)
fdm.load_model(MODEL_NAME)
fdm.load_ic(IC_PATH, False)

fdm.set_dt(SIM_DT)
fdm.run_ic()

pub = FDMPublisher(
    host = "tcp://127.0.0.1",
    port = 5555,
    topic = "topic/jsbsim", 
    time_sleep_s = 0.8*SIM_DT,
    debug = False)

step = 0
# fdm.run()


fdm[prp.gear_all_cmd.name] = 0
fdm[prp.throttle_cmd.name] = 0.75

# catalog = fdm.query_property_catalog("propulsion")

roll_controller = PIDController(1.0, 0.5, 1, SIM_DT)
pitch_controller = PIDController(K_P = 1.0, K_I = 0.1, K_D = 0.1,dt=SIM_DT)
rudder_controller = PIDController(0.5, 0.5, 1, SIM_DT)
vel_controller = PIDController(dt = SIM_DT)


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

    
    


