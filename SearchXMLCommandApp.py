from SearchXMLCommand import SearchXMLCommand
from tkinter import *
from tkinter import messagebox

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        sys.exit()

root = Tk()
root.title("Search DPP XMLCommand")
SearchXMLCommand(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
root.destroy()
