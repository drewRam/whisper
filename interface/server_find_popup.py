from tkinter import *
from . import DARK_BLUE, SHINY_WHITE, LABEL_STYLE

class ServerFindPopup(Toplevel):
    def __init__(self, master: Frame, var_to_set: StringVar):
        super().__init__(master)
        self.var_to_set = var_to_set
        self.num_of_ip_choices = 0

        self.chosen_server_ip = StringVar(self)
        self.search_status = StringVar(self, "Searching...")

        self.search_status_label = Label(self, textvariable=self.search_status)

        self.select_server = Button(self, text="Select server", command=self.select_choice)
        self.cancel_button = Button(self, text="Cancel", command=self.destroy)

        self.found_ip_frame = Frame(self)

        self.style()
        self.grid()

    def grid(self):
        self.search_status_label.grid(row=0, columnspan=2)

        self.found_ip_frame.grid(row=1, columnspan=2)

        self.select_server.grid(row=2, column=0)
        self.cancel_button.grid(row=2, column=1)

    def style(self):
        self.search_status_label.configure(**LABEL_STYLE)

        self.select_server.configure(highlightbackground=DARK_BLUE)
        self.cancel_button.configure(highlightbackground=DARK_BLUE)

        self.found_ip_frame.configure(bg=DARK_BLUE)

        self.configure(bg=DARK_BLUE, padx=10, pady=10)

    def add_choice(self, ip_found):
        new_button = Radiobutton(self.found_ip_frame, text=ip_found,
            variable=self.chosen_server_ip, value=ip_found)

        new_button.configure(bg=DARK_BLUE, fg=SHINY_WHITE)

        new_button.grid(row=self.num_of_ip_choices)
        self.num_of_ip_choices += 1

    def select_choice(self):
        if self.chosen_server_ip.get != '':
            self.var_to_set.set(self.chosen_server_ip.get())
            self.destroy()

    def set_status_done(self):
        self.search_status.set("Finished Search")