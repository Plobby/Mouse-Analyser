from tkinter import *
import iomanager
counter = 0

def import_video():
   iomanager.get_videos(True)


def close_window(): 
    root.destroy()

def open_settings():
    Toplevel(settings)

root = Tk()
root.title("Welcome to MouseHUB!")
root.geometry('1200x720')
root.configure(background='black')

settings = Tk()
settings.title("Settings")
settings.geometry("800x600")
settings.configure(background='black')

window = Label(root, text="MouseHUB")
window.pack()   

btn = Button(window, text="Import Video", width=25, bg="orange", command = import_video)
btn.grid(column=1, row=99)

btn1 = Button(window, text="Settings", bg="orange", width=25, command= open_settings)
btn1.grid(column=2, row=99)

btn2 = Button(window, text="Exit", width=50, command = close_window)
btn2.grid(column=3, row=99)


root.mainloop()
