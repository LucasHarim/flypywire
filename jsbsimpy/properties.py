import math
from typing import List, Union, Dict, NewType
import collections
import jsbsim
from jsbsimpy.formatting import make_valid_name

FT_TO_M = 0.3048
PropertyName = NewType("PropertyName", str)

class BoundedProperty(collections.namedtuple('BoundedProperty', ['name', 'description', 'min', 'max'])):
    
    @property
    def valid_name(self) -> str:
        return make_valid_name(self.name)

    def __call__(self) -> PropertyName:
        return self.name

class Property(collections.namedtuple('Property', ['name', 'description'])):
    
    @property
    def valid_name(self) -> str:
        return make_valid_name(self.name)

    def __call__(self) -> PropertyName:
        return self.name

def get_outputs_from_fdm(
    fdm: jsbsim.FGFDMExec,
    properties: List[Union[Property, BoundedProperty]]) -> Dict[str, float]:
    
    return {prop.name: fdm[prop.name] for prop in properties}


# position and attitude
altitude_sl_ft = BoundedProperty('position/h-sl-ft', 'altitude above mean sea level [ft]', -1400, 85000)
altitude_sl_m = BoundedProperty('position/h-sl-meters', 'altitude above mean sea level [m]', -1400 * FT_TO_M, 85000 * FT_TO_M)
altitude_agl_ft = BoundedProperty('position/h-agl-ft', 'altitude above ground level [ft]', 0, 85000)
lat_geod_deg = BoundedProperty('position/lat-geod-deg', 'geocentric latitude [deg]', -90, 90)
lng_geoc_deg = BoundedProperty('position/long-gc-deg', 'geodesic longitude [deg]', -180, 180)
dist_from_start_lon_mt = Property('position/distance-from-start-lon-mt', 'distance travelled along the longitudinal axis from starting position [m]')
dist_from_start_lat_mt = Property('position/distance-from-start-lat-mt', 'distance travelled along the latitudinal axis from starting position [m]')
dist_travel_m = Property('position/distance-from-start-mag-mt', 'distance travelled from starting position [m]')

pitch_rad = BoundedProperty('attitude/pitch-rad', 'pitch [rad]', -0.5 * math.pi, 0.5 * math.pi)
roll_rad = BoundedProperty('attitude/roll-rad', 'roll [rad]', -math.pi, math.pi)
yaw_rad = BoundedProperty('attitude/psi-rad', 'psi [rad]', -math.pi, math.pi)
heading_deg = BoundedProperty('attitude/psi-deg', 'heading [deg]', 0, 360)

sideslip_deg = BoundedProperty('aero/beta-deg', 'sideslip [deg]', -180, +180)


# velocities
u_fps = BoundedProperty('velocities/u-fps', 'body frame x-axis velocity [ft/s]', -2200, 2200)
v_fps = BoundedProperty('velocities/v-fps', 'body frame y-axis velocity [ft/s]', -2200, 2200)
w_fps = BoundedProperty('velocities/w-fps', 'body frame z-axis velocity [ft/s]', -2200, 2200)
v_north_fps = BoundedProperty('velocities/v-north-fps', 'velocity true north [ft/s]', float('-inf'), float('+inf'))
v_east_fps = BoundedProperty('velocities/v-east-fps', 'velocity east [ft/s]', float('-inf'), float('+inf'))
v_down_fps = BoundedProperty('velocities/v-down-fps', 'velocity downwards [ft/s]', float('-inf'), float('+inf'))
p_radps = BoundedProperty('velocities/p-rad_sec', 'roll rate [rad/s]', -2 * math.pi, 2 * math.pi)
q_radps = BoundedProperty('velocities/q-rad_sec', 'pitch rate [rad/s]', -2 * math.pi, 2 * math.pi)
r_radps = BoundedProperty('velocities/r-rad_sec', 'yaw rate [rad/s]', -2 * math.pi, 2 * math.pi)
altitude_rate_fps = Property('velocities/h-dot-fps', 'Rate of altitude change [ft/s]')


# controls state
aileron_left = BoundedProperty('fcs/left-aileron-pos-norm', 'left aileron position, normalised', -1, 1)
aileron_right = BoundedProperty('fcs/right-aileron-pos-norm', 'right aileron position, normalised', -1, 1)
elevator = BoundedProperty('fcs/elevator-pos-norm', 'elevator position, normalised', -1, 1)
rudder = BoundedProperty('fcs/rudder-pos-norm', 'rudder position, normalised', -1, 1)
throttle = BoundedProperty('fcs/throttle-pos-norm', 'throttle position, normalised', 0, 1)

flight_controls = [aileron_left, aileron_right, elevator, rudder, throttle]

gear = BoundedProperty('gear/gear-pos-norm', 'landing gear position, normalised', 0, 1)

# engines
engine_running = Property('propulsion/engine/set-running', 'engine running (0/1 bool)')
all_engines_running = Property('propulsion/set-running', 'set engine running (-1 for all engines)')
engine_thrust_lbs = Property('propulsion/engine/thrust-lbs', 'engine thrust [lb]')

# controls command
aileron_cmd = BoundedProperty('fcs/aileron-cmd-norm', 'aileron commanded position, normalised', -1., 1.)
elevator_cmd = BoundedProperty('fcs/elevator-cmd-norm', 'elevator commanded position, normalised', -1., 1.)
rudder_cmd = BoundedProperty('fcs/rudder-cmd-norm', 'rudder commanded position, normalised', -1., 1.)
throttle_cmd = BoundedProperty('fcs/throttle-cmd-norm', 'throttle commanded position, normalised', 0., 1.)
mixture_cmd = BoundedProperty('fcs/mixture-cmd-norm', 'engine mixture setting, normalised', 0., 1.)
throttle_1_cmd = BoundedProperty('fcs/throttle-cmd-norm[1]', 'throttle 1 commanded position, normalised', 0., 1.)
mixture_1_cmd = BoundedProperty('fcs/mixture-cmd-norm[1]', 'engine mixture 1 setting, normalised', 0., 1.)
gear_all_cmd = BoundedProperty('gear/gear-cmd-norm', 'all landing gear commanded position, normalised', 0, 1)

# simulation
sim_dt = Property('simulation/dt', 'JSBSim simulation timestep [s]')
sim_time_s = Property('simulation/sim-time-sec', 'Simulation time [s]')

# initial conditions
initial_altitude_ft = Property('ic/h-sl-ft', 'initial altitude MSL [ft]')
initial_terrain_altitude_ft = Property('ic/terrain-elevation-ft', 'initial terrain alt [ft]')
initial_longitude_geoc_deg = Property('ic/long-gc-deg', 'initial geocentric longitude [deg]')
initial_latitude_geod_deg = Property('ic/lat-geod-deg', 'initial geodesic latitude [deg]')

initial_u_fps = Property('ic/u-fps', 'body frame x-axis velocity; positive forward [ft/s]')
initial_v_fps = Property('ic/v-fps', 'body frame y-axis velocity; positive right [ft/s]')
initial_w_fps = Property('ic/w-fps', 'body frame z-axis velocity; positive down [ft/s]')

initial_phi_deg = Property('ic/phi-deg', 'Initial roll angle [deg]')
initial_theta_deg = Property('ic/theta-deg', 'Initial pitch angle [deg]')
initial_psi_deg = Property('ic/psi-deg', 'Initial yaw angle [deg]')

initial_p_radps = Property('ic/p-rad_sec', 'roll rate [rad/s]')
initial_q_radps = Property('ic/q-rad_sec', 'pitch rate [rad/s]')
initial_r_radps = Property('ic/r-rad_sec', 'yaw rate [rad/s]')
initial_roc_fpm = Property('ic/roc-fpm', 'initial rate of climb [ft/min]')
initial_heading_deg = Property('ic/psi-true-deg', 'initial (true) heading [deg]')

# Turbulence
_turb_description = '''
        0: ttNone (turbulence disabled)
        1: ttStandard
        2: ttCulp
        3: ttMilspec (Dryden spectrum)
        4: ttTustin (Dryden spectrum)
    '''

turbulence_type = Property('atmosphere/turb-type', f'Turbulence type selection. {_turb_description}')
turb_milspec_windspeed_at_20ft_AGL_fps = Property('atmosphere/turbulence/milspec/windspeed_at_20ft_AGL-fps', 'Parameter for Milspec and Tustin turbulence types')
turb_milspec_severity = Property('atmosphere/turbulence/milspec/severity', 'Parameter for Milspec and Tustin turbulence types')

# Wind
gust_down_fps = Property('atmosphere/gust-down-fps', 'Gust down [ft/s]')
gust_east_fps = Property('atmosphere/gust-east-fps', 'Gust from East [ft/s]')
gust_north_fps = Property('atmosphere/gust-north-fps', 'Gust from North [ft/s]')
headwind_fps = Property('atmosphere/headwind-fps', 'Headwind [ft/s]')


DEFAULT_FDM_OUTPUTS = [
    sim_time_s,
    altitude_sl_ft,
    altitude_agl_ft,
    lat_geod_deg,
    lng_geoc_deg,
    roll_rad,
    pitch_rad,
    heading_deg,
    u_fps,
    v_fps,
    w_fps,
    dist_from_start_lat_mt,
    dist_from_start_lon_mt]
