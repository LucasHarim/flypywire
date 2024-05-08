from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from jsbsimpy.fdm_pubsub import FDMSubscriber
from jsbsimpy import properties as prp
from jsbsimpy.client.queue_thread import make_queue_and_thread, on_queue_data

import numpy as np

if __name__ == '__main__':
        
    sub = FDMSubscriber(
        host = "tcp://127.0.0.1",
        port = 5555,
        topic = 'topic/jsbsim',
        debug=False)
    
    
    
    time = [0, 0]
    pitch = [0, 0]
    roll = [0, 0]
    
    params = {"max_time": -1, "max_pitch": -1}
    min_time = 0
    min_pitch = -1

    def get_fdm_output(i):
    
        global min_time, min_pitch

        fdm_outputs = sub.rcv_fdm_outputs(output_dtype=dict)
        if fdm_outputs: 
            
            time.append(fdm_outputs[prp.sim_time_s.name])
            pitch.append(fdm_outputs[prp.pitch_rad.name])
            roll.append(fdm_outputs[prp.roll_rad.name])

        if max(time) > 0.75 * params['max_time']: 
            params['max_time'] = 2*max(time)
            
        if max(pitch) > params['max_pitch']:

            params['max_pitch'] = 1.5 * max(pitch)
            min_pitch = 0.5 * max(pitch)
            
        plt.cla()
        plt.xlim([max(max(time) - 10, 0), max(time) + 5])
        
        # plt.ylim([-np.pi/2, np.pi/2])
        # plt.plot(time, pitch, label = "Pitch [rad]")
        plt.plot(time, roll, label = "Roll [rad]")
        
        

        
        plt.grid(True)
        plt.legend()


    ani = FuncAnimation(plt.gcf(), get_fdm_output, interval = 2)    
    
    # plt.tight_layout()
    
    plt.show()


        






