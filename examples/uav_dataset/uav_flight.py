import argparse
import cv2
import pandas as pd
import math
from flypywire import (
    ActorState,
    SimulationState)
import flypywire.unityapi as unity

def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = 2.0 * (w * x + y * z)
        t1 = 1.0 - 2.0 * (x**2 + y**2)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

df = pd.read_csv("examples/uav_dataset/flight1_data.csv", sep=',', dtype=float)

select = [
    'position_x',
    'position_y',
    'position_z',
    'orientation_x',
    'orientation_y',
    'orientation_z',
    'orientation_w']

times = df['time']
states = df.drop(labels = [col for col in df.columns.to_list() if col not in select], axis=1)
z_offset = 1
origin = unity.GeoCoordinate(float(states['position_y'][0]), float(states['position_x'][0]), float(states['position_z'][0] + z_offset))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser('UAV-Flight')
    parser.add_argument('-v', '--video', help = 'Enable video streaming', action = 'store_true')
    parser.add_argument('-r', '--record', help = 'If video streaming is enabled, records the video and save as output.avi', action='store_true')
    
    args = parser.parse_args()
    
    if args.video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can try 'MJPG', 'XVID', etc.
        out = cv2.VideoWriter('output.avi', fourcc, 60.0, (640, 480))

    client = unity.Client()

    with client.RenderContext() as ctx:

        uav = unity.GameObject('uav', 'Assets/UAVs/DJIM300')
        
        ctx.set_origin(origin)
        ctx.spawn_gameobject(uav, geocoordinate=origin)
        # time.sleep(10)
        # if args.video:
        ctx.spawn_camera('uav-cam', uav, transform=unity.Transform(position = unity.Vector3(y=0.15, z = 0.15), rotation = unity.Vector3(30)))
        
        cam = unity.Camera()

        for i in range(len(times)):
            
            if args.video:
                if cam.is_connected:
                    frame = cam.get_image()
                    if args.record: 
                        out.write(frame)
                    cv2.imshow('Camera', frame)
                    
                    if cv2.waitKey(1) == ord('q'):
                        break
    
            x_ang, y_ang, z_ang = euler_from_quaternion(states['orientation_x'][i], states['orientation_y'][i], states['orientation_z'][i], states['orientation_w'][i])
            state_float64 =  [states['position_y'][i], states['position_x'][i], states['position_z'][i] + z_offset,
                            x_ang, y_ang, z_ang]
            
            state_float = [float(val) for val in state_float64]
            
            ctx.publish_simulation_state(
                SimulationState(
                    float(times[i]), {
                        uav.name: ActorState(*state_float)
                    }
                ),
                0.05
            )
            
    cv2.destroyAllWindows()
    if args.record: out.release()

            