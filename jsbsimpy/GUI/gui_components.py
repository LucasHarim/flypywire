from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkFont,
    CTkEntry)

    
        
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

        self.latitude_entry = CTkEntry(self.loc_frame, placeholder_text = 'latitude')
        self.latitude_entry.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.longitude_entry = CTkEntry(self.loc_frame, placeholder_text = 'longitude')
        self.longitude_entry.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.altitude_frame = CTkFrame(self)
        self.altitude_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)

        self.alt_label = CTkLabel(self.altitude_frame, text = "Altitude [ft]",
            compound = 'center' , font = CTkFont(size = 12))
        self.alt_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        
        self.altitude_entry = CTkEntry(self.altitude_frame, placeholder_text = 'altitude')
        self.altitude_entry.grid(row = 1, column = 0, padx = 5, pady = 5)


        _vel_frame_rows = iter(range(10))

        self.vel_frame = CTkFrame(self)
        self.vel_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.loc_label = CTkLabel(self.vel_frame, text = "Velocity - Body frame [ft/s]",
            compound = 'center' , font = CTkFont(size = 12))
        self.loc_label.grid(row = next(_vel_frame_rows), column = 0, padx = 10, pady = 10)

        self.ubody_entry = CTkEntry(self.vel_frame, placeholder_text = 'ubody')
        self.ubody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        self.vbody_entry = CTkEntry(self.vel_frame, placeholder_text = 'vbody')
        self.vbody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        self.wbody_entry = CTkEntry(self.vel_frame, placeholder_text = 'wbody')
        self.wbody_entry.grid(row = next(_vel_frame_rows), column = 0, padx = 5, pady = 5)

        _attitude_frame_rows = iter(range(10))


        self.attitude_frame = CTkFrame(self)
        self.attitude_frame.grid(row = next(_main_frame_rows), column = 0, padx = 5, pady = 5)
        
        self.att_label = CTkLabel(self.attitude_frame, text = "Attitude - [deg]",
            compound = 'center' , font = CTkFont(size = 12))
        self.att_label.grid(row = next(_attitude_frame_rows), column = 0, padx = 10, pady = 10)

        self.phi_entry = CTkEntry(self.attitude_frame, placeholder_text = 'phi')
        self.phi_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

        self.theta_entry = CTkEntry(self.attitude_frame, placeholder_text = 'theta')
        self.theta_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

        self.psi_entry = CTkEntry(self.attitude_frame, placeholder_text = 'psi')
        self.psi_entry.grid(row = next(_attitude_frame_rows), column = 0, padx = 5, pady = 5)

    def _setup_frame(self) -> None:

        ...


class MainFrame(CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)