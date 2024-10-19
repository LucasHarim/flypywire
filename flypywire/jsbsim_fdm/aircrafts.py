import jsbsim
from dataclasses import dataclass
from flypywire import unityapi as unity
from flypywire.jsbsim_fdm.basic_initial_conditions import setup_cruise_condition

@dataclass
class AircraftTemplate:

    jsbsim_name: str
    asset_path: str
    rolename: str = ""

    def get_actor(self, rolename: str) -> unity.GameObject:
        self.rolename = rolename
        return unity.Actor(rolename, self.asset_path)
    
    def fdm_cruise(self, origin: unity.GeoCoordinate) -> jsbsim.FGFDMExec:
        return setup_cruise_condition(self.jsbsim_name, origin)
    
    
F16 = AircraftTemplate('f16', 'Assets/Airplanes/F16')
F22 = AircraftTemplate('f22', 'Assets/Airplanes/F22')
B747 = AircraftTemplate('B747', 'Assets/Airplanes/USAF747')
B787 = AircraftTemplate('787-8', 'Assets/Airplanes/B787')
A320 = AircraftTemplate('A320', 'Assets/Airplanes/A320')
T38 = AircraftTemplate('T38', 'Assets/Airplanes/T38')
C172 = AircraftTemplate('c172p', 'Assets/Airplanes/Cessna172')
T6 = AircraftTemplate('t6texan2', 'Assets/Airplanes/BeechcraftT6II')
J3CUB = AircraftTemplate('J3Cub', 'Assets/Airplanes/PiperPA18')
GLIDER = AircraftTemplate('SGS', 'Assets/Gliders/Glider01')

_aircraft_list = [F16, F22, T38, T6, B747, A320, B787, C172, J3CUB, GLIDER]
aircraft_collection = {a.jsbsim_name: a for a in _aircraft_list}