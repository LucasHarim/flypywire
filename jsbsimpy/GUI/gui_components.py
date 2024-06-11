import os
from collections import namedtuple
import asyncio
from numpy import round
from jsbsim import FGFDMExec
from typing import List, Iterable, Union, Type, Callable, Any
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkFont,
    CTkEntry,
    CTkComboBox)


class CTkEntryTyped(CTkEntry):

    def __init__(self, master, valid_type: Union[float, int, str] = str, **kwargs):
    
        super().__init__(master, **kwargs)
        
        self.valid_type = valid_type
        self.bind("<KeyRelease>", self.validate_type)
    
    def validate_type(self, event=None) -> None:
        
        if self.get():
            
            entry_value = self.get()

            if self.valid_type == int:
                
                if not entry_value.isdigit():
                    
                    # If the entry content is not a digit, remove the last character
                    self.delete(len(entry_value)-1, 'end')
            
            if self.valid_type == float:
                
                if entry_value != '-':
                    try:
                        float(entry_value)
                    except ValueError:
                        # If the entry content is not a valid float, remove the last character
                        self.delete(len(entry_value)-1, 'end')
    

    def get_value(self):

        if self.valid_type == int: return int(self.get())

        elif self.valid_type == float: return float(self.get())

        else: return self.get()


NameCTkComponent = namedtuple('NameCTkComponent', ['name', 'component'])

class MyCTkFrame(CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        self._ctk_components: List[NameCTkComponent] = list()
        
        
    def get_inputs_from_components(self) -> dict:
        
        _typed_entries = {obj.name: obj.component.get_value() for obj in self._ctk_components if isinstance(obj.component, CTkEntryTyped)}
        _non_typed_entries = {obj.name: obj.component.get() for obj in self._ctk_components if not isinstance(obj.component, CTkEntryTyped)}
        
        return {**_non_typed_entries, **_typed_entries}
        

class NavigationFrame(MyCTkFrame):

    def __init__(self, master,**kwargs):

        super().__init__(master, **kwargs)
        
        
        self._setup_frame()

        self.frame_label = CTkLabel(self, text = "Menu", compound='center', 
            font = CTkFont(size=15, weight='bold'))

        self.frame_label.grid(row=0, column=0, padx = 20, pady = 20)
        
        self.sim_button = CTkButton(self, corner_radius=0,
            height=40, border_spacing=10, text="Simulation", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command= lambda: print('Simulation Button pressed'))

        self.sim_button.grid(row=1, column=0, sticky="ew")

    def _setup_frame(self) -> None:

        self.grid_rowconfigure(4, weight=1)


class InitialConditionFrame(MyCTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        _main_frame_rows = iter(range(10))

        self.frame_label = CTkLabel(self, text = "Initial Conditions",
            compound = 'center' , font = CTkFont(size = 12, weight='bold'))
        self.frame_label.grid(row = next(_main_frame_rows), column = 0, padx = 10, pady = 10)

        self.loc_frame = CTkFrame(self)
        self.loc_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.loc_label = CTkLabel(self.loc_frame, text = "Location [deg]",
            compound = 'center' , font = CTkFont(size = 12))
        self.loc_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.latitude_entry = CTkEntryTyped(self.loc_frame, valid_type=float ,placeholder_text = 'latitude')
        self.latitude_entry.insert(0, 0.0)
        self.latitude_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        

        self.longitude_entry = CTkEntryTyped(self.loc_frame, valid_type=float,placeholder_text = 'longitude')
        self.longitude_entry.insert(0, 0.0)
        self.longitude_entry.grid(row = 2, column = 0, padx = 5, pady = 5)
        

        self.altitude_frame = CTkFrame(self)
        self.altitude_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)

        self.alt_label = CTkLabel(self.altitude_frame, text = "Altitude [ft]",
            compound = 'center' , font = CTkFont(size = 12))
        self.alt_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        
        self.altitude_entry = CTkEntryTyped(self.altitude_frame, valid_type=float,placeholder_text = 'altitude')
        self.altitude_entry.insert(0, 5000.0)
        self.altitude_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        
        _vel_frame_rows = iter(range(10))

        self.vel_frame = CTkFrame(self)
        self.vel_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.vel_label = CTkLabel(self.vel_frame, text = "Velocity - Body frame [ft/s]",
            compound = 'center' , font = CTkFont(size = 12))
        self.vel_label.grid(row = next(_vel_frame_rows), column = 0, padx = 10, pady = 10)

        self.ubody_entry = CTkEntryTyped(self.vel_frame, valid_type=float,placeholder_text = 'ubody')
        self.ubody_entry.insert(0, 100.0)
        self.ubody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        self.vbody_entry = CTkEntryTyped(self.vel_frame, valid_type=float,placeholder_text = 'vbody')
        self.vbody_entry.insert(0, 0.0)
        self.vbody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        self.wbody_entry = CTkEntryTyped(self.vel_frame, valid_type=float,placeholder_text = 'wbody')
        self.wbody_entry.insert(0, 0.0)
        self.wbody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        _attitude_frame_rows = iter(range(10))


        self.attitude_frame = CTkFrame(self)
        self.attitude_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.att_label = CTkLabel(self.attitude_frame, text = "Attitude - [deg]",
            compound = 'center' , font = CTkFont(size = 12))
        self.att_label.grid(row = next(_attitude_frame_rows), column = 0, padx = 10, pady = 10)

        self.phi_entry = CTkEntryTyped(self.attitude_frame, valid_type=float, placeholder_text = 'phi')
        self.phi_entry.insert(0, 0.0)
        self.phi_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

        self.theta_entry = CTkEntryTyped(self.attitude_frame, valid_type=float,placeholder_text = 'theta')
        self.theta_entry.insert(0, 0.0)
        self.theta_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

        self.psi_entry = CTkEntryTyped(self.attitude_frame, valid_type = float,placeholder_text = 'psi')
        self.psi_entry.insert(0, 0.0)
        self.psi_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)
        
        self._ctk_components += [
            self.latitude_entry,
            self.longitude_entry,
            self.altitude_entry,
            self.ubody_entry,
            self.vbody_entry,
            self.wbody_entry,
            self.phi_entry,
            self.theta_entry,
            self.psi_entry]
        
        self._ctk_components = [NameCTkComponent(component._placeholder_text, component) for component in self._ctk_components]

class AircraftFrame(MyCTkFrame):

    def __init__(self, master, jsbsim_root: str, **kwargs) -> None:

        self.jsbsim_root = jsbsim_root
        self.aircraft_path = os.path.join(self.jsbsim_root, 'aircraft')
        self.available_aircrafts_in_root = self._get_aircrafts_in_jsbsim_root()

        super().__init__(master, **kwargs)
        
        _frame_rows = iter(range(10))

        self.frame_label = CTkLabel(self, text = 'Aircraft', compound='center', font = CTkFont(size = 12, weight='bold'))
        self.frame_label.grid(row = next(_frame_rows), column = 0, padx = 10, pady = 10)
        
        self.aircraft_selection = CTkComboBox(self, values = [aircraft for aircraft in self.available_aircrafts_in_root])
        self.aircraft_selection.grid(row = next(_frame_rows), column = 0, padx = 10, pady = 5)

        self._ctk_components += [self.aircraft_selection]
    
    def _get_aircrafts_in_jsbsim_root(self) -> List[str]:
        
        try:
    
            # List all entries in the given path
            entries = os.listdir(self.aircraft_path)
            
            # Filter out only directories
            directories = [entry for entry in entries if os.path.isdir(os.path.join(self.aircraft_path, entry))]
    
            return directories

        except FileNotFoundError:
            return f"The path {self.aircraft_path} does not exist."

        except PermissionError:
            return f"Permission denied for accessing the path {self.aircraft_path}."
    
    
    
    def outputs(self) -> dict:


        return {'aircraft_selected': self.aircraft_selection.get()}
    

class SocketConfigFrame(MyCTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        
        _frame_rows = iter(range(10))

        self.frame_label = CTkLabel(self, text = 'Socket configuration', font = CTkFont(size = 12, weight='bold'))
        self.frame_label.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        
        
        self.host_entry = CTkEntryTyped(self, placeholder_text='host')
        self.host_entry.insert(0, 'tcp://127.0.0.1')
        self.host_entry.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        self.host_entry.bind("<KeyRelease>", self.display_address)

        self.port_entry = CTkEntryTyped(self, valid_type=int,placeholder_text='port')
        self.port_entry.insert(0, 5555)
        self.port_entry.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        self.port_entry.bind("<KeyRelease>", self.display_address)

        self.address_label = CTkLabel(self, text = 'host:port', font = CTkFont(size = 12), compound='left')
        self.address_label.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        
        self._ctk_components += [NameCTkComponent(component._placeholder_text, component)\
                for component in [self.host_entry, self.port_entry]]
            
    def display_address(self, event = None) -> None:
        
        self.address_label.configure(text = f'Address: {self.host_entry.get()}:{self.port_entry.get()}')
    

class StartButton(CTkButton):

    def __init__(self, master, fdm_exec: FGFDMExec, text: str = "Start", **kwargs):

        super().__init__(master,text = text, **kwargs)
        
        self.fdm_exec = fdm_exec
        
        
        
        # self.button = CTkButton(self, text = text)
        # self.button.grid()
        # self.button.configure(command = lambda: self.start_tasks())    

        self.sim_info_label = CTkLabel(self, text='', font = CTkFont(size = 12))
        self.sim_info_label.grid(row = 1, column = 0, padx = 5, pady = 5)
        
        self.loop = asyncio.get_event_loop()
        self.tasks = [
            self.loop.create_task(self.run_fdm_loop(self.fdm_exec)),
        ]

    
    async def run_fdm_loop(self, fdm: FGFDMExec) -> None:
        
        self.fdm_exec.run_ic()

        while True: 

            fdm.run()
            print(round(self.fdm_exec['simulation/sim-time-sec'], 3))
            
            await asyncio.sleep(0.5)
    
    
    async def update_label(self) -> None:
        self.sim_info_label.configure(
            text = ''.join(['Simulation time: ',str(round(self.fdm_exec['simulation/sim-time-sec'], 3)), ' seconds']))
    
    def start_tasks(self) -> None:

        self.loop.run_until_complete(asyncio.wait(self.tasks))
        self.loop.close()

        

        

class MainFrame(MyCTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

if __name__ == '__main__':


    s = SocketConfigFrame(None)
    
    