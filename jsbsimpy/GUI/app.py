import customtkinter
from typing import Tuple

from jsbsimpy.GUI.gui_components import (
	NavigationFrame,
	InitialConditionFrame,
	AircraftFrame,
	SocketConfigFrame)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

	def __init__(self, title: str, dimensions: Tuple[int, int], jsbsim_root: str):

		self.jsbsim_root = jsbsim_root

		super().__init__()
        
		self.title(title)
		self.geometry = f'{dimensions[0]}x{dimensions[1]}'
		self.resizable(width=False, height=False)
		
		# configure grid layout (4x4)
		# self.grid_columnconfigure(1, weight=1)
		# self.grid_columnconfigure((2, 3), weight=0)
		# self.grid_rowconfigure((0, 1, 2), weight=1)
		
		_frame_rows = iter(range(100))
		_frame_columns = iter(range(100))

		
		self.nav_frame = NavigationFrame(self)
		self.nav_frame.grid(row=next(_frame_rows), column=next(_frame_columns), padx = 10, pady = 10, sticky="nsew")
		
		self.aicraft_frame = AircraftFrame(self, jsbsim_root = self.jsbsim_root)
		self.aicraft_frame.grid(row = 0, column = next(_frame_columns), padx = 10, pady = (10, 0))

		self.ic_frame = InitialConditionFrame(self)
		self.ic_frame.grid(row = 0, column = next(_frame_columns), padx = 10, pady = 10,sticky="ns")
		
		self.socket_config_frame = SocketConfigFrame(self)
		self.socket_config_frame.grid(row = 0, column = next(_frame_columns), padx = 10, pady = 10)
		

if __name__ == '__main__':
	
	_JSBSim_ROOT = 'C:\\Users\\harim\\AppData\\Local\\JSBSim'
    
	app = App(
		title="Just Flying",
		dimensions = (1100, 550),
		jsbsim_root=_JSBSim_ROOT)

	app.mainloop()


