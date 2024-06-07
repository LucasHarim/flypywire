import os
from typing import List, Iterable, Union
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkFont,
    CTkEntry,
    CTkComboBox)


class CTkEntryType(CTkEntry):

    def __init__(self, master, valid_type: Union[float, int, str] = str, **kwargs):
    
        super().__init__(master, **kwargs)
        
        self.valid_type = valid_type
        self.bind("<KeyRelease>", self.validate_type)
    
    def validate_type(self, event=None):
        
        entry_value = self.get()
        if self.get():
            
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
            

class NavigationFrame(CTkFrame):

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


class InitialConditionFrame(CTkFrame):

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

        self.latitude_entry = CTkEntryType(self.loc_frame, valid_type=float ,placeholder_text = 'latitude')
        self.latitude_entry.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.longitude_entry = CTkEntryType(self.loc_frame, valid_type=float,placeholder_text = 'longitude')
        self.longitude_entry.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.altitude_frame = CTkFrame(self)
        self.altitude_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)

        self.alt_label = CTkLabel(self.altitude_frame, text = "Altitude [ft]",
            compound = 'center' , font = CTkFont(size = 12))
        self.alt_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        
        self.altitude_entry = CTkEntryType(self.altitude_frame, valid_type=float,placeholder_text = 'altitude')
        self.altitude_entry.grid(row = 1, column = 0, padx = 5, pady = 5)


        _vel_frame_rows = iter(range(10))

        self.vel_frame = CTkFrame(self)
        self.vel_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.loc_label = CTkLabel(self.vel_frame, text = "Velocity - Body frame [ft/s]",
            compound = 'center' , font = CTkFont(size = 12))
        self.loc_label.grid(row = next(_vel_frame_rows), column = 0, padx = 10, pady = 10)

        self.ubody_entry = CTkEntryType(self.vel_frame, valid_type=float,placeholder_text = 'ubody')
        self.ubody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        self.vbody_entry = CTkEntryType(self.vel_frame, valid_type=float,placeholder_text = 'vbody')
        self.vbody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        self.wbody_entry = CTkEntryType(self.vel_frame, valid_type=float,placeholder_text = 'wbody')
        self.wbody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        _attitude_frame_rows = iter(range(10))


        self.attitude_frame = CTkFrame(self)
        self.attitude_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.att_label = CTkLabel(self.attitude_frame, text = "Attitude - [deg]",
            compound = 'center' , font = CTkFont(size = 12))
        self.att_label.grid(row = next(_attitude_frame_rows), column = 0, padx = 10, pady = 10)

        self.phi_entry = CTkEntryType(self.attitude_frame, valid_type=float, placeholder_text = 'phi')
        self.phi_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

        self.theta_entry = CTkEntryType(self.attitude_frame, valid_type=float,placeholder_text = 'theta')
        self.theta_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

        self.psi_entry = CTkEntryType(self.attitude_frame, valid_type = float,placeholder_text = 'psi')
        self.psi_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)
        
    
    def outputs(self) -> dict:
        
        _outputs = {
            'Location': {
                'latitude': self.latitude_entry.get(),
                'longitude': self.longitude_entry.get()},
        }


class AircraftFrame(CTkFrame):

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

        # self.aircraft_selection_label = CTkLabel(self.aircraft_selection, text = '')
        # self.aircraft_selection.grid(row = 0, column = 10, padx = 10, pady = 10)
    
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
    

class SocketConfigFrame(CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        
        _frame_rows = iter(range(10))

        self.frame_label = CTkLabel(self, text = 'Socket configuration', font = CTkFont(size = 12, weight='bold'))
        self.frame_label.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        
        
        self.host_entry = CTkEntryType(self, placeholder_text='host')
        self.host_entry.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        self.host_entry.bind("<KeyRelease>", self.display_address)

        self.port_entry = CTkEntryType(self, valid_type=int,placeholder_text='port')
        self.port_entry.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        self.port_entry.bind("<KeyRelease>", self.display_address)

        self.address_label = CTkLabel(self, text = '', font = CTkFont(size = 12), compound='left')
        self.address_label.grid(row = next(_frame_rows), column = 0, padx = 5, pady = 5)
        
    def display_address(self, event = None) -> None:
        
        self.address_label.configure(text = f'Address: {self.host_entry.get()}:{self.port_entry.get()}')
    
    
        

class MainFrame(CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)