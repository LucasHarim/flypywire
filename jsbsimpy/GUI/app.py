import os
import time
from enum import Enum, auto
from numpy import round
from threading import Thread
import customtkinter
from customtkinter import CTkButton
from typing import Tuple
from jsbsim import FGFDMExec

from jsbsimpy import properties as prp
from jsbsimpy.GUI.gui_components import (
	NavigationFrame,
	InitialConditionFrame,
	AircraftFrame,
	SocketConfigFrame,
	StartButton,
	TabView,
	SettingsWindow)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class SimState(Enum):
	START = auto()
	PAUSE = auto()
	STOP = auto()

class App(customtkinter.CTk):

	def __init__(self, title: str, dimensions: Tuple[int, int], jsbsim_root: str):

		self.jsbsim_root = jsbsim_root
		self.fdm_exec = FGFDMExec(root_dir = self.jsbsim_root)
		self.fdm_thread = Thread(target = self.start_sim, daemon=True)
		IC_PATH = 'examples\\beechcraft_t6_cruise_lensois.xml'
		# self.fdm_exec.load_ic(IC_PATH, False)

		super().__init__()
        
		self.title(title)
		self.dimensions = dimensions
		self.geometry = f'{dimensions[0]}x{dimensions[1]}'
		self.resizable(width=False, height=False)
		
		# configure grid layout (4x4)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure((2, 3), weight=0)
		self.grid_rowconfigure((0, 1, 2), weight=1)
		
		_frame_rows = iter(range(100))
		_frame_columns = iter(range(100))

		
		self.nav_frame = NavigationFrame(self)
		self.nav_frame.grid(row=next(_frame_rows), column=next(_frame_columns), padx = 10, pady = 10, sticky="nsew")
		
		
		# _tab_frame_columns = iter(range(100))
		# self.tabs = TabView(self)
		# self.tabs.grid(row = 0, column = next(_frame_columns), padx = 20, pady = 20)
		
		
		# self.ic_frame = InitialConditionFrame(self.tabs.tab("Initial Condition"))
		# self.ic_frame.grid(row = 0, column = next(_tab_frame_columns), padx = 10, pady = 10,sticky="ns")
		
		# self.socket_config_frame = SocketConfigFrame(self.tabs.tab("Aircraft"))
		# self.socket_config_frame.grid(row = 0, column = next(_tab_frame_columns), padx = 10, pady = 10)
		
		self.start_btn = StartButton(self.nav_frame, text = 'Start Simulation', on_click = lambda: [self.fdm_thread.start() for _ in range(1) if not self.fdm_thread.is_alive()])
		self.start_btn.grid(row = self.nav_frame.settings_button.grid_info()['row'] + 1 , column = 0, padx = 10, pady = 10)
		
		self.settings_window = SettingsWindow(master = self, jsbsim_root=self.jsbsim_root, width = 350)
		self.nav_frame.settings_button.configure(command = self.open_settings_window)
		

	@property
	def entries(self) -> dict:
		return {**self.settings_window.entries}
	
	@property
	def sim_state(self) -> SimState: #TODO: move the states to StartButton class
		return SimState.START
	
	def open_settings_window(self) -> None:

		if not self.settings_window._is_window_active: self.settings_window.init_window()
	
	def stop_fdm_thread(self) -> None: self.fdm_thread.join()

	def load_aircraft(self) -> None:

		self.fdm_exec.load_model(self.entries.get('aircraft'))
	
	
	def parse_ic_and_other_properties(self) -> None:
		
		[self.fdm_exec.set_property_value(property_name, self.entries.get(property_name))\
		for property_name in self.entries.keys() if property_name.startswith('ic/')]
		
		[self.fdm_exec.set_property_value(property_name, self.entries.get(property_name))\
		for property_name in self.entries.keys() if (not property_name.startswith('ic/') and '/' in property_name)]
		
		self.fdm_exec.run_ic()
	
	
	def start_sim(self) -> None:

		self.load_aircraft()
		self.parse_ic_and_other_properties()

		while True:
			
			if self.sim_state == SimState.START:
				
				self.fdm_exec.run()
				
				time.sleep(0.1)
				print(round(self.fdm_exec['simulation/sim-time-sec'], 3))
			
			elif self.sim_state == SimState.PAUSE:

				self.fdm_exec.hold()
			
			else: break
				
		self.stop_fdm_thread()
	


	
if __name__ == '__main__':
	
	
    
	app = App(
		title="Just Flying",
		dimensions = (880, 550),
		jsbsim_root = os.environ.get('JSBSIM_ROOT'))

	app.mainloop()
	


