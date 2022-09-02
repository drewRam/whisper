from .style_constants import DARK_BLUE, SHINY_WHITE, LABEL_STYLE
from tkinter import *
import socket
import re

IP_PATTERN = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

class CreateServerMenu(Frame):
	def __init__(self, master=None, create_server_function=print, server_ip="127.0.0.1"):
		super().__init__(master)

		self.server_create = create_server_function

		self.port_value = StringVar(self)
		self.username_val = StringVar(self)
		self.error_val = StringVar(self)

		self.menu_label = Label(self, text="Create a server")
		self.error_label = Label(self, textvariable=self.error_val)
		self.port_entry_label = Label(self, text="Port #")
		self.username_entry_label = Label(self, text="Username: ")

		self.port_entry = Entry(self, textvariable=self.port_value)
		self.username_entry = Entry(self, textvariable=self.username_val)

		self.create_server_button = Button(self, text="Create Server", command=self.try_to_create_server)

		self.style()

	def style(self):
		self.menu_label.configure(**LABEL_STYLE)
		self.error_label.configure(fg="red", bg=DARK_BLUE)
		self.port_entry_label.configure(**LABEL_STYLE)
		self.username_entry_label.configure(**LABEL_STYLE)
		
		self.port_entry.configure(highlightthickness=0)
		self.username_entry.configure(highlightthickness=0)
		
		self.create_server_button.configure(highlightbackground=DARK_BLUE)
		
		self.configure(bg=DARK_BLUE)		


	def grid(self, *args, **kwargs):
		super().grid(*args, **kwargs)

		self.menu_label.grid(row=0, column=0, columnspan=2)
		
		self.error_label.grid(row=1, column=0, columnspan=2)

		self.port_entry_label.grid(row=2, column=0, sticky=W)
		self.port_entry.grid(row=2, column=1, sticky=W)

		self.username_entry_label.grid(row=3, column=0, sticky=W)
		self.username_entry.grid(row=3, column=1, sticky=W)

		self.create_server_button.grid(row=4, column=0, columnspan=2)

	def try_to_create_server(self):
		port = self.port_value.get()
		username = self.username_val.get()

		if len(port) != 4 or not port.isnumeric() or int(port) <= 1024:
			self.error_val.set("Port must be a 4-digit # over 1024")
		elif len(username) == 0:
			self.error_val.set("Please enter a username")
		else:
			port = int(port)
			self.server_create(port, username)

class CreateClientMenu(Frame):
	def __init__(self, master=None, create_client_function=print, client_ip="127.0.0.1"):
		super().__init__(master)

		self.client_create = create_client_function
		
		self.port_value = StringVar(self)
		self.username_val = StringVar(self)
		self.server_ip_val = StringVar(self)
		self.error_val = StringVar(self)

		self.menu_label = Label(self, text="Enter server information")
		self.error_label = Label(self, textvariable=self.error_val, fg="red")
		self.server_ip_label = Label(self, text="Server IP")
		self.port_entry_label = Label(self, text="Port #")
		self.username_entry_label = Label(self, text="Username: ")

		self.server_ip_entry = Entry(self, textvariable=self.server_ip_val)		
		self.port_entry = Entry(self, textvariable=self.port_value)		
		self.username_entry = Entry(self, textvariable=self.username_val)

		self.create_server_button = Button(self, text="Connect to Server", command=self.try_to_create_client)

		self.style()

	def style(self):
		self.menu_label.configure(**LABEL_STYLE)
		self.error_label.configure(fg='red', bg=DARK_BLUE)
		self.server_ip_label.configure(**LABEL_STYLE)	
		self.port_entry_label.configure(**LABEL_STYLE)
		self.username_entry_label.configure(**LABEL_STYLE)

		self.server_ip_entry.configure(highlightthickness=0)	
		self.port_entry.configure(highlightthickness=0)
		self.username_entry.configure(highlightthickness=0)
		
		self.create_server_button.configure(highlightbackground=DARK_BLUE)

		self.configure(bg=DARK_BLUE)

	def grid(self, *args, **kwargs):
		super().grid(*args, **kwargs)

		self.menu_label.grid(row=0, column=0, columnspan=2)

		self.error_label.grid(row=1, column=0, columnspan=2)

		self.server_ip_label.grid(row=2, column=0, sticky=W)
		self.server_ip_entry.grid(row=2, column=1, sticky=W)

		self.port_entry_label.grid(row=3, column=0, sticky=W)
		self.port_entry.grid(row=3, column=1, sticky=W)

		self.username_entry_label.grid(row=4, column=0, sticky=W)
		self.username_entry.grid(row=4, column=1, sticky=W)

		self.create_server_button.grid(row=5, column=0, columnspan=2)

	def try_to_create_client(self):
		ip = self.server_ip_val.get()
		port = self.port_value.get()
		username = self.username_val.get()

		if len(port) != 4 or not port.isnumeric() or int(port) <= 1024:
			self.error_val.set("Port must be a 4-digit # over 1024")
		elif not re.match(IP_PATTERN, ip):
			self.error_val.set("IP must be a valid IPv4 address.")
		elif len(username) == 0:
			self.error_val.set("Please enter a username")
		else:
			port = int(port)
			self.client_create(ip, port, username)