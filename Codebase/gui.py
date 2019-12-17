from tkinter import *
import iomanager
counter = 0

def import_video():
    iomanager.get_videos(True)

def close_window(): 
    root.destroy()

root = Tk()
root.title("Welcome to MouseHUB!")
root.geometry('1200x720')

window = Label(root, text="MouseHUB")
window.pack()

btn = Button(window, text="Import Video", width=25, command = import_video)
btn.grid(column=1, row=5)

btn1 = Button(window, text="Settings", width=25)
btn1.grid(column=2, row=5)

btn2 = Button(window, text="Exit", width=50, command = close_window)
btn2.grid(column=3, row=5)


root.mainloop()
