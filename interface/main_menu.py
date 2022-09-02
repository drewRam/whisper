from tkinter import *
from .style_constants import SHINY_WHITE, DARK_BLUE

class MainMenu(Frame):
	def __init__(self, master: Frame, join_function, create_function):
		super().__init__(master)

		self.serving_port = StringVar(self)
		self.username = StringVar(self)

		self.app_label = Label(self, text="Murmur")

		self.join_server_button = Button(self, text="Join a server", command=join_function)
		self.start_server_button = Button(self, text="Start a server", command=create_function)

		self.style()

	def style(self):
		self.app_label.configure(bg=DARK_BLUE, fg=SHINY_WHITE)

		self.join_server_button.configure(highlightbackground=DARK_BLUE)
		self.start_server_button.configure(highlightbackground=DARK_BLUE)

		self.configure(bg=DARK_BLUE)

	def grid(self, *args, **kwargs):
		super().grid(*args, **kwargs)

		self.app_label.grid(row=0, column=0, columnspan=2)

		self.join_server_button.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)

		self.start_server_button.grid(row=2, column=0, columnspan=2, sticky=N+S+E+W)