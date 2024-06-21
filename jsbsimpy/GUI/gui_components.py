import os
from collections import namedtuple
import time
from numpy import round
from jsbsim import FGFDMExec
import jsbsimpy.properties as prp
from typing import List, Iterable, Union, Type, Callable, Tuple, Dict
import customtkinter as ctk

class TypedEntry(ctk.CTkEntry):

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


class MyCTkFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        self._ctk_components: Dict[str, ctk.CTkBaseClass] = list()
        
        
    def get_inputs_from_components(self) -> dict:
        
        _typed_entries = {name: component.get_value() for name, component in self._ctk_components.items() if isinstance(component, TypedEntry)}
        _non_typed_entries = {name: component.get() for name, component in self._ctk_components.items() if not isinstance(component, TypedEntry)}
        
        return {**_non_typed_entries, **_typed_entries}
    
class MyScrollableFrame(ctk.CTkScrollableFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        self._ctk_components: Dict[str, ctk.CTkBaseClass] = list()
        
        
    def get_inputs_from_components(self) -> dict:
        
        _typed_entries = {name: component.get_value() for name, component in self._ctk_components.items() if isinstance(component, TypedEntry)}
        _non_typed_entries = {name: component.get() for name, component in self._ctk_components.items() if not isinstance(component, TypedEntry)}
        
        return {**_non_typed_entries, **_typed_entries}


class NavigationFrame(MyCTkFrame):

    def __init__(self, master,**kwargs):

        super().__init__(master, **kwargs)
        
        
        self.frame_label = ctk.CTkLabel(self, text = "Menu", compound='center', 
            font = ctk.CTkFont(size=15, weight='bold'))
        
        self.frame_label.grid(row=0, column=0, padx = 5, pady = 5)
        
        self.sim_button = ctk.CTkButton(self, corner_radius=0,
            height=40, border_spacing=10, text="Simulation", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command= lambda: print('Simulation Button pressed'))

        self.sim_button.grid(row=1, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self, corner_radius=0,
            height=40, border_spacing=10, text="Settings", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command= lambda: print('Settings Button pressed'))
        
        self.settings_button.grid(row = 2, sticky = 'ew')



def make_labeled_entry(
        master,
        label_text: str,
        font,
        placeholder_text = '',
        row: int = 0, column: int = 0,
        valid_type = float, 
        default_value = None, **kwargs) -> TypedEntry:
    
    
    entry = TypedEntry(master, valid_type=valid_type, placeholder_text = placeholder_text)
    entry.grid(row = row, column = column, **kwargs)
    if default_value != None: entry.insert(0, default_value)

    label = ctk.CTkLabel(master, text = label_text, font = font, compound='left')
    label.grid(row = entry.grid_info()['row'], column = 0)
    
    return entry

class TabView(ctk.CTkTabview):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        
        self.initial_condition_tab = self.add("Initial Condition")
        self.aircraft_tab = self.add("Aircraft")


        self.set("Initial Condition")



class InitialConditionFrame(MyCTkFrame):
    
    ##TODO make persistent IC

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        _main_frame_rows = iter(range(100))

        self.frame_label = ctk.CTkLabel(self, text = "Initial Conditions",
            compound = 'center' , font = ctk.CTkFont(size = 12, weight='bold'))
        # self.frame_label.grid(column = next(_main_frame_rows), row = 0, padx = 10, pady = 2)
        
        _sys_frame_rows = iter(range(10))

        self.sys_frame = ctk.CTkFrame(self)
        self.sys_frame.grid(row = next(_main_frame_rows), padx = 5, pady = 5, sticky = 'ew')
        self.sys_label = ctk.CTkLabel(self.sys_frame, text = "Systems",
            compound = 'center' , font = ctk.CTkFont(size = 12, weight='bold'))
        self.sys_label.grid(padx = 10, pady = 10)
        
        
        self.landing_gear_switch = ctk.CTkSwitch(
            self.sys_frame,
            text = '',
            onvalue = 1,
            offvalue = 0)
        
        self.landing_gear_switch.grid(row = next(_sys_frame_rows), column = 1, padx=5, pady = 5)
        self.lg_label = ctk.CTkLabel(self.sys_frame, text='Landing Gear', font = ctk.CTkFont(size=12))
        self.lg_label.grid(row = self.landing_gear_switch.grid_info()['row'], column = 0)

        self.engines_switch = ctk.CTkSwitch(
            self.sys_frame,
            text = '',
            onvalue = -1,
            offvalue = 0)
        
        self.engines_switch.select() ## Selected by default
        self.engines_switch.grid(row = next(_sys_frame_rows), column = 1, padx=5, pady = 5)
        self.eng_label = ctk.CTkLabel(self.sys_frame, text='Engines running', font = ctk.CTkFont(size=12))
        self.eng_label.grid(row = self.engines_switch.grid_info()['row'], column = 0, padx=5, pady=5)
        
        self.throttle_slider = ctk.CTkSlider(
            self.sys_frame,
            from_ = 0,
            to = 1,
            number_of_steps=20,
            command = lambda event: self.throttle_label.configure(text= f"Throtle: {round(float(self.throttle_slider.get()), 2)}"),
            progress_color='blue')
        
        self.throttle_slider.grid(row = next(_sys_frame_rows), column = 1,padx = 5, pady = 5)
        self.throttle_slider.set(0.75)

        self.throttle_label = ctk.CTkLabel(self.sys_frame,
                text = f'Throttle: {self.throttle_slider.get()}',
                font = ctk.CTkFont(size = 12), compound='left')
        
        self.throttle_label.grid(row = self.throttle_slider.grid_info()['row'], column = 0)
        

        self.loc_frame = ctk.CTkFrame(self)
        self.loc_frame.grid(row = next(_main_frame_rows), padx = 5, pady = 5, sticky='ew')
        self.loc_label = ctk.CTkLabel(self.loc_frame, text = "Geopositioning",
            compound = 'center' , font = ctk.CTkFont(size = 12, weight='bold'))
        self.loc_label.grid(padx = 10, pady = 10)

        self.latitude_entry = make_labeled_entry(
            self.loc_frame, 
            placeholder_text = 'latitude',
            font = ctk.CTkFont(size = 10),
            label_text='Latitude [deg]',
            row = 1, column = 1, padx = 5, pady=5)

        self.longitude_entry = make_labeled_entry(
            self.loc_frame, 
            placeholder_text = 'longitude',
            font = ctk.CTkFont(size = 10),
            label_text='Longitude [deg]',
            # default_value = 0.0,
            row = 2, column = 1, padx = 5, pady=5)
        
        
        self.altitude_entry = make_labeled_entry(
            self.loc_frame, 
            placeholder_text = 'altitude',
            font = ctk.CTkFont(size = 10),
            label_text='Altitude [ft]',
            # default_value = 1000.0,
            row = 3, column = 1, padx = 5, pady=5)
        
        self.heading_entry = make_labeled_entry(
            self.loc_frame, 
            placeholder_text = 'True heading',
            font = ctk.CTkFont(size = 10),
            label_text='Heading [deg]',
            # default_value = 0.0,
            row = 4, column = 1, padx = 5, pady=5)
        
        
        _vel_frame_rows = iter(range(10))

        self.vel_frame = ctk.CTkFrame(self)
        self.vel_frame.grid(row = next(_main_frame_rows), padx = 5, pady = 5, sticky='ew')
        
        self.vel_label = ctk.CTkLabel(self.vel_frame, text = "Velocity - Body frame",
            compound = 'left' , font = ctk.CTkFont(size = 12, weight='bold'))
        self.vel_label.grid(row = next(_vel_frame_rows), column = 0, padx = 10, pady = 10)

        
        self.ubody_entry = make_labeled_entry(
            self.vel_frame, 
            placeholder_text = 'ubody',
            font = ctk.CTkFont(size = 10),
            label_text='ubody [ft/s]',
            # default_value = 200.0,
            row = next(_vel_frame_rows), column = 1, padx = 5, pady=5)
        
        self.vbody_entry = make_labeled_entry(
            self.vel_frame, 
            placeholder_text = 'vbody',
            font = ctk.CTkFont(size = 10),
            label_text='vbody [ft/s]',
            # default_value = 0.0,
            row = next(_vel_frame_rows), column = 1, padx = 5, pady=5)
        
        self.wbody_entry = make_labeled_entry(
            self.vel_frame, 
            placeholder_text = 'wbody',
            font = ctk.CTkFont(size = 10),
            label_text='wbody [ft/s]',
            # default_value = 0.0,
            row = next(_vel_frame_rows), column = 1, padx = 5, pady=5)
        
        _attitude_frame_rows = iter(range(10))

        self.attitude_frame = ctk.CTkFrame(self)
        self.attitude_frame.grid(row = next(_main_frame_rows), padx = 5, pady = 5, sticky='ew')
        
        self.att_label = ctk.CTkLabel(self.attitude_frame, text = "Attitude",
            compound = 'center' , font = ctk.CTkFont(size = 12, weight='bold'))
        self.att_label.grid(row = next(_attitude_frame_rows), column = 0, padx = 10, pady = 10)

        self.phi_entry = make_labeled_entry(
            self.attitude_frame, 
            placeholder_text = 'phi',
            font = ctk.CTkFont(size = 10),
            label_text='phi [deg]',
            # default_value = 0.0,
            row = next(_attitude_frame_rows), column = 1, padx = 5, pady=5)
        
        self.theta_entry = make_labeled_entry(
            self.attitude_frame, 
            placeholder_text = 'theta',
            font = ctk.CTkFont(size = 10),
            label_text='theta [deg]',
            # default_value = 0.0,
            row = next(_attitude_frame_rows), column = 1, padx = 5, pady=5)
        
        self.psi_entry = make_labeled_entry(
            self.attitude_frame, 
            placeholder_text = 'psi',
            font = ctk.CTkFont(size = 10),
            label_text='psi [deg]',
            # default_value = 0.0,
            row = next(_attitude_frame_rows), column = 1, padx = 5, pady=5)
        
        self._ctk_components = {
            prp.gear.name: self.landing_gear_switch,
            prp.all_engines_running.name: self.engines_switch,    
            prp.throttle_cmd.name: self.throttle_slider,
            prp.initial_latitude_geod_deg.name: self.latitude_entry,
            prp.initial_longitude_geoc_deg.name: self.longitude_entry,
            prp.initial_altitude_ft.name: self.altitude_entry,
            prp.initial_heading_deg.name: self.heading_entry,
            prp.initial_u_fps.name: self.ubody_entry,
            prp.initial_v_fps.name: self.vbody_entry,
            prp.initial_w_fps.name: self.wbody_entry,
            prp.initial_phi_deg.name: self.phi_entry,
            prp.initial_theta_deg.name: self.theta_entry,
            prp.initial_psi_deg.name: self.psi_entry,

        }
    

class AircraftFrame(MyCTkFrame):

    def __init__(self, master, jsbsim_root: str, **kwargs) -> None:

        self.jsbsim_root = jsbsim_root
        self.aircraft_path = os.path.join(self.jsbsim_root, 'aircraft')
        self.available_aircrafts_in_root = self._get_aircrafts_in_jsbsim_root()

        super().__init__(master, **kwargs)
        
        _frame_rows = iter(range(10))

        self.frame_label = ctk.CTkLabel(self, text = 'Aircraft', compound='center', font = ctk.CTkFont(size = 12, weight='bold'))
        self.frame_label.grid(row = next(_frame_rows), column = 0, padx = 10, pady = 10)
        
        self.aircraft_selection = ctk.CTkComboBox(self, values = [aircraft for aircraft in self.available_aircrafts_in_root])
        self.aircraft_selection.grid(row = next(_frame_rows), column = 0, padx = 10, pady = 5, sticky = 'ew')

        self._ctk_components = {'aircraft': self.aircraft_selection}
    
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
    
    
    

class SocketConfigFrame(MyCTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        
        _frame_rows = iter(range(10))

        self.frame_label = ctk.CTkLabel(self, text = 'Socket configuration', font = ctk.CTkFont(size = 12, weight='bold'))
        self.frame_label.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.host_entry = TypedEntry(self, placeholder_text='host')
        self.host_entry.insert(0, 'tcp://127.0.0.1')
        self.host_entry.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        self.host_entry.bind("<KeyRelease>", self.display_address)

        self.port_entry = TypedEntry(self, valid_type=int,placeholder_text='port')
        self.port_entry.insert(0, 5555)
        self.port_entry.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        self.port_entry.bind("<KeyRelease>", self.display_address)

        self.address_label = ctk.CTkLabel(self, text = f'{self.host_entry.get()}:{self.port_entry.get()}', font = ctk.CTkFont(size = 12), compound='left')
        self.address_label.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        
        self._ctk_components = {component._placeholder_text: component\
                for component in [self.host_entry, self.port_entry]}
            
    def display_address(self, event = None) -> None:
        
        self.address_label.configure(text = f'{self.host_entry.get()}:{self.port_entry.get()}')
    
class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, master, jsbsim_root: str,dimensions: Tuple[int, int] = None,**kwargs):
        
        self.master = master
        self.jsbsim_root = jsbsim_root
        self.kwargs = kwargs
        self.dimensions = dimensions
        
        self._is_window_active = False
        self._opened_once_flag = False

        self.entries = self.default_settings
        
    
    @property
    def default_settings(self) -> dict:

        return {
            'aircraft': 'A320',
            prp.gear(): 0,
            prp.all_engines_running(): -1,    
            prp.throttle_cmd(): 0.75,
            prp.initial_latitude_geod_deg(): 0.0,
            prp.initial_longitude_geoc_deg(): 0.0,
            prp.initial_altitude_ft(): 5000,
            prp.initial_heading_deg(): 0.0,
            prp.initial_u_fps(): 200.0,
            prp.initial_v_fps(): 0.0,
            prp.initial_w_fps(): 0.0,
            prp.initial_phi_deg(): 0.0,
            prp.initial_theta_deg(): 0.0,
            prp.initial_psi_deg(): 0.0
        }

    def init_window(self) -> None:
        
        super().__init__(self.master ,**self.kwargs)
        
        if self.dimensions: self.geometry(f'{self.dimensions[0]}x{self.dimensions[1]}')
        self.title('Settings')
        self.resizable(width=False, height=False)
        self.focus
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.scrollable = MyScrollableFrame(self, fg_color='transparent',  width=350, height = 600)
        self.scrollable.pack(padx = 5, pady = 5)
        
        self.aicraft_frame = AircraftFrame(self.scrollable, jsbsim_root = self.jsbsim_root)
        self.aicraft_frame.grid(row = 0,padx = 10, pady = 10, sticky = 'ew')

        self.ic_frame = InitialConditionFrame(self.scrollable)
        self.ic_frame.grid(row = 1, padx = 10, pady = 10)
        
        self.setup_settings()
        
        # self.grab_set()
        
        self._is_window_active = True
        self._opened_once_flag = True

    def setup_settings(self) -> None:
        
        
        [self.ic_frame._ctk_components[name].insert(0, value) for name, value in self.default_settings.items()\
            if (name in self.ic_frame._ctk_components.keys() and not isinstance(self.ic_frame._ctk_components[name]), (ctk.CTkSwitch, ctk.CTkSlider))]
    

    def get_inputs_from_components(self) -> dict:
        
        return {**self.aicraft_frame.get_inputs_from_components(), **self.ic_frame.get_inputs_from_components()}
        
        

    def on_closing(self) -> None:
        
        print('parsing settings...')
        self.entries = self.get_inputs_from_components()
        self._is_window_active = False
        self.destroy()
        

    
class StartButton(ctk.CTkButton):
    
    def __init__(self, master, on_click: Callable[[None], None], text: str = "Start",  **kwargs):

        super().__init__(master,text = text, **kwargs)
        
        self.configure(command= on_click)
        self.sim_info_label = ctk.CTkLabel(self, text='', font = ctk.CTkFont(size = 12))
        self.sim_info_label.grid(row = 1, column = 0, padx = 5, pady = 5)

    def run_fdm_loop(self, fdm: FGFDMExec) -> None:
        
        self.fdm_exec.run_ic()

        while True: 

            fdm.run()
            self.update_label()
            time.sleep(0.1)
            
            
    def update_label(self) -> None:
        self.sim_info_label.configure(
            text = ''.join(['Simulation time: ',str(round(self.fdm_exec['simulation/sim-time-sec'], 3)), ' seconds']))
    
    def start_task(self) -> None:
        ...
        

        

        

class MainFrame(MyCTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

if __name__ == '__main__':


    ...
    
    