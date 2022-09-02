from tkinter import *
from .style_constants import SHINY_WHITE, DARK_BLUE, LABEL_STYLE

class ClientView(Frame):
	def __init__(self, master=None, send_function=print):
		super().__init__(master)
		self.send_function = send_function

		self.message_display = Text(self, width=45, wrap=WORD, bg=SHINY_WHITE)
		self.message_entry = Text(self, width=30, height=5, wrap=WORD, bg=SHINY_WHITE)
		
		self.send_button = Button(self, text="Send", command=lambda:self.send_message(None))

		self.message_entry.bind("<Return>", self.send_message)

		self.style()

	def style(self):
		self.configure(bg=DARK_BLUE)

		for widget in self.winfo_children():
			widget.configure(highlightthickness=0)

		self.message_display.configure(state=DISABLED)
		self.send_button.configure(highlightbackground=DARK_BLUE)

	def grid(self, *args, **kwargs):
		super().grid(*args, **kwargs)

		self.message_display.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

		self.message_entry.grid(row=1, column=0, sticky=N+S+E+W, padx=5, pady=(0,5))
		self.send_button.grid(row=1, column=1, sticky=N+S+E+W, padx=5, pady=(0,5))

	def send_message(self, event: object):
		to_send = self.message_entry.get('1.0', 'end')
		
		if len(to_send.strip()) > 0:
			self.message_entry.delete('1.0', 'end')
			self.send_function(to_send.strip())
		
		return 'break' # Disables newline entry 

	def write_to_screen(self, text: str):
		pos = self.message_display.yview()[1]

		self.message_display['state'] = NORMAL
		self.message_display.insert('end', text + '\n')
		self.message_display['state'] = DISABLED

		if pos > 0.90:
			self.message_display.yview_moveto(1.0)