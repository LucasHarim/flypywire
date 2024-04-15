import jsbsim
import numpy as np
from jsbsimpy import properties as prp
from jsbsimpy.fdm_pubsub import FDMPublisher


ROOT_DIR = 'C:\\Users\\harim\\AppData\\Local\\JSBSim'
IC_PATH = 'examples\\basic_ic.xml'
MODEL_NAME = 'A320'
SIM_DT = 0.03


fdm = jsbsim.FGFDMExec(root_dir = ROOT_DIR)
fdm.load_model(MODEL_NAME)
fdm.load_ic(IC_PATH, False)

fdm.set_dt(SIM_DT)
fdm.run_ic()

pub = FDMPublisher(
    host = "tcp://127.0.0.1",
    port = 5555,
    topic = "topic/jsbsim", 
    time_sleep_s = 0.02,
    debug = False)

step = 0
fdm.run()

fdm[prp.throttle_cmd.name] = 1

# catalog = fdm.query_property_catalog("propulsion")

fdm[prp.throttle.name] = 0.85

_cmd_done = False

while True:
    
    
    time = fdm[prp.sim_time_s.name]
    
    fdm[prp.aileron_cmd.name] = 0.08 * np.sin(time)
    # fdm[prp.elevator_cmd.name] = 0.1 * np.cos(time)
    fdm[prp.rudder_cmd.name] = 0.1 * np.sin(time)
    
    # if (time > 5 and not _cmd_done): 
        
    #     fdm[prp.aileron_cmd.name] = 0.05
    
    # if (time > 10): fdm[prp.aileron_cmd.name] = -0.1
    
    
    
    fdm.run()
    
    fdm_outputs = prp.get_outputs_from_fdm(fdm, prp.DEFAULT_FDM_OUTPUTS)
    pub.publish_fdm_outputs(fdm_outputs= {"step": step, **fdm_outputs}, realtime=True)
    step += 1 

    
    


