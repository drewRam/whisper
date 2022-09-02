import tkinter
import logging
from app import App

if __name__ == '__main__':
    logging.basicConfig(filename='console.log', level=logging.INFO)
    logging.info("\n==Application starting\n")

    root = tkinter.Tk()
    App(root)

    root.mainloop()