from SearchXMLCommand import SearchXMLCommand
from tkinter import *
from tkinter import messagebox

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        sys.exit()

root = Tk()
#root.geometry('900x250')
root.title("Search DPP XMLCommand")
app = SearchXMLCommand(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
root.destroy()
