from tkinter import *
import sys
import iomanager

# Function to import videos
def import_video():
    iomanager.get_videos(True)

# Function to show the gui and start the main loop
def show_gui():
    gui.deiconify()
    gui.mainloop()
    
# Function to hide the gui
def hide_gui():
    gui.withdraw()

# Function to remove the gui and exit the application
def remove_gui():
    gui.destroy()
    sys.exit(0)

# Function to show the settings window
def show_settings():
    settings.deiconify()

# Function to hide the settings window
def hide_settings():
    settings.withdraw()

# Setup the main GUI interface
gui = Tk()
gui.title("Welcome to MouseHUB!")
gui.geometry('1200x720')
gui.configure(background='black')

# Pack window
window = Label(gui, text="MouseHUB")
window.pack()

# import button
btn_import = Button(window, text="Import Video", width=25, bg="orange", command = import_video)
btn_import.grid(column=1, row=99)
# Settings button
btn_settings = Button(window, text="Settings", bg="orange", width=25, command = show_settings)
btn_settings.grid(column=2, row=99)
# Close button
btn_close = Button(window, text="Exit", width=50, command = remove_gui)
btn_close.grid(column=3, row=99)

# Override close action to just hide window
gui.protocol("WM_DELETE_WINDOW", remove_gui)

# Hide the gui window
hide_gui()

# Setup the settings interface
settings = Tk()
settings.title("Settings")
settings.geometry("800x600")
settings.configure(background='black')

# Override the close action
settings.protocol("WM_DELETE_WINDOW", hide_settings)

# Hide the settings window
hide_settings()