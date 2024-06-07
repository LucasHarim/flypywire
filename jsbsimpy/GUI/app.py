import customtkinter
from typing import Tuple

from jsbsimpy.GUI.gui_components import (
	NavigationFrame,
	InitialConditionFrame)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

	def __init__(self, title: str, dimensions: Tuple[int, int]):

		super().__init__()
        
		self.title(title)
		self.geometry = f'{dimensions[0]}x{dimensions[1]}'
        
		# configure grid layout (4x4)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure((2, 3), weight=0)
		self.grid_rowconfigure((0, 1, 2), weight=1)

		self.nav_frame = NavigationFrame(self)
		self.nav_frame.grid(row=0, column=0, padx = 10, pady = 10, sticky="nsew")

		self.ic_frame = InitialConditionFrame(self)
		self.ic_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky="ns")

if __name__ == '__main__':

    app = App(
        title="My app",
        dimensions = (1100, 550))
    
    app.mainloop()


