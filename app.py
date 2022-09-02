import tkinter
from interface import *
from server import Server
from client import Client

class App:
    def __init__(self, root:tkinter):
        self.root = root
        self.root.resizable(False, False)
        self.root.configure(padx=10, pady=10, bg=DARK_BLUE)
        self.root.title("Mutter")

        self.current_frame = MainMenu(self.root,
                                self.create_client_menu,
                                self.create_server_menu)
        self.current_frame.grid()

    def create_server_menu(self):
        self.replace_current_frame(CreateServerMenu(self.root, self.spawn_server))

    def create_client_menu(self):
        self.replace_current_frame(CreateClientMenu(self.root, self.spawn_client))

    def spawn_client(self, ip: str, port: int, username: str):
        self.client_instance = Client("0.0.0.0", ip, print, port)
        self.replace_current_frame(ClientView(self.root, self.client_instance.send))

        self.client_instance.process = self.current_frame.write_to_screen
        self.client_instance.connect(username)

    def spawn_server(self, port: int, username: str):
        self.server_instance = Server(port, "0.0.0.0", print)

        self.replace_current_frame(ClientView(self.root, self.server_instance.send_as_hosting_user))
        self.server_instance.client_process = self.current_frame.write_to_screen
        self.server_instance.start_processing()

        self.server_instance.register_hosting_client(username)

    def replace_current_frame(self, new_frame:Frame):
        self.current_frame.grid_forget()
        self.current_frame.destroy()

        self.current_frame = new_frame
        self.current_frame.grid()