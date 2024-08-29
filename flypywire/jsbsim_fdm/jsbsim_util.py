import os
from typing import List

JSBSIM_ROOT = os.environ.get('JSBSIM_ROOT')

def get_aircraft_list(jsbsim_root: str) -> List[str]:

    _aircraft_dir = os.path.join(jsbsim_root, 'aircraft')
    
    try:

        # List all entries in the given path
        dir_names = os.listdir(_aircraft_dir)
        
        # Filter out only directories
        aircrafts = [aircraft_name for aircraft_name in dir_names if os.path.isdir(os.path.join(_aircraft_dir, aircraft_name))]

        return aircrafts

    except FileNotFoundError:
        print(f"The path {_aircraft_dir} does not exist.")
    

    except PermissionError:
        print(f"Permission denied for accessing the path {_aircraft_dir}.")
    
    return list()
    