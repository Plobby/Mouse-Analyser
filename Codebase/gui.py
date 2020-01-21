import tkinter as tk
import iomanager
from PIL import ImageTk, Image

# Load images
TitleLabelImage = ImageTk.PhotoImage(Image.open("../Assets/TitleBar.jpg"))
SettingsImage = ImageTk.PhotoImage(Image.open("../Assets/SettingsBar.jpg"))
SettingsHoverImage = ImageTk.PhotoImage(Image.open("../Assets/SettingsHover.jpg"))
VideoImage = ImageTk.PhotoImage(Image.open("../Assets/VideoBar.jpg"))
VideoHoverImage = ImageTk.PhotoImage(Image.open("../Assets/VideoHover.jpg"))
ExitImage = ImageTk.PhotoImage(Image.open("../Assets/ExitBar.jpg"))
ExitHoverImage = ImageTk.PhotoImage(Image.open("../Assets/ExitHover.jpg"))
SmthingImage = ImageTk.PhotoImage(Image.open("../Assets/DataBar.jpg"))

# Function to import videos
def import_video():
   iomanager.get_videos(True)

# Function to show the GUI
def show_window():
    app = Pages()
    app.title("MouseHUB")
    app.geometry("1280x720")
    app.minsize(700, 500)
    app.protocol("WM_DELETE_WINDOW", close_window)
    app.mainloop()

# Function to close the GUI
def close_window():
    # Exits program
    raise SystemExit

# Pages Code From = https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
class Pages(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Call superclass function
        tk.Toplevel.__init__(self, *args, **kwargs)

        # Configure resizing options through grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create toolbar
        add_toolbar(self, self)

        # Create container
        container = tk.Frame(self)
        container.grid(column=0, row=1, sticky="nesw")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Empty frames object and add new frames
        self.frames = {}
        for f in (VideoPage, DataPage, SettingsPage):
            frame = f(self, container)
            self.frames[f] = frame
            frame.grid(row=1, column=0, sticky="nesw")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
        
        # Show the first frame
        self.show_frame(VideoPage)

    # Shows the frame from frame name
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Allows variables between the pages, requires self.controller = controller
    def get_page(self, page_class):
        return self.frames[page_class]

# Function to add the navigation bar
def add_toolbar(container, controller):
    # Assign the container controller
    container.controller = controller
    # Frame for the title bar
    title_bar_frame = tk.Frame(container, bg="#646464")
    title_bar_frame.grid(row=0, column=0, sticky="nesw")
    # Set expanding values
    title_bar_frame.grid_rowconfigure(0, weight=0)
    title_bar_frame.grid_columnconfigure(0, weight=0)
    title_bar_frame.grid_columnconfigure(1, weight=1)
    title_bar_frame.grid_columnconfigure(2, weight=0)
    # Shows Title in Top Right
    TitleLabel = tk.Label(title_bar_frame, image=TitleLabelImage, bd=0, highlightthickness=0)
    TitleLabel.grid(row=0, column=0)
    # Expanding to fill space
    filler_frame = tk.Frame(title_bar_frame, bg="#646464")
    filler_frame.grid(row=0, column=1)
    # Frame for the buttons
    button_frame = tk.Frame(title_bar_frame)
    button_frame.grid(row=0, column=2)
    # Shows Video Page Button m in Menu
    VideoButton = tk.Button(button_frame, image=VideoImage,command=lambda: controller.show_frame(VideoPage), bd=0, highlightthickness=0)
    VideoButton.grid(row=0, column=0)
    # Shows ???? Page Button in Menu
    SmthingButton = tk.Button(button_frame, image=SmthingImage,command=lambda: controller.show_frame(DataPage), bd=0, highlightthickness=0)
    SmthingButton.grid(row=0, column=1)
    # Shows Settings Page Button in Menu
    SettingsButton = tk.Button(button_frame, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage), bd=0, highlightthickness=0)
    SettingsButton.grid(row=0, column=2)
    # Shows last item in Menu
    ExitButton = tk.Button(button_frame, image=ExitImage, command = close_window,bd=0, highlightthickness=0,)
    ExitButton.grid(row=0, column=3)

class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        # Call superclass function
        tk.Frame.__init__(self, parent, bg="#848484")
        # Configure resizing
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # Import Video Function
        PlayVideoButton = tk.Button(self, text="Import", command=import_video)
        PlayVideoButton.grid(row=0, column=0)
        # Placeholder canvas for video playback
        VideoFrame = tk.Canvas(self, bg="black", highlightbackground="#646464")
        VideoFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nes")

class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        # Call superclass function
        tk.Frame.__init__(self, parent)

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        # Call superclass function
        tk.Frame.__init__(self, parent)

# Code to do hover images, need to find a better way to implement it.
"""
        def Video_on_enter(e):
            VideoButton['image'] = VideoHoverImage
        def Video_on_leave(e):
            VideoButton['image'] = VideoImage
        VideoButton.bind("<Enter>", Video_on_enter)
        VideoButton.bind("<Leave>", Video_on_leave)
        def Settings_on_enter(e):
            SettingsButton['image'] = SettingsHoverImage
        def Settings_on_leave(e):
            SettingsButton['image'] = SettingsImage
        SettingsButton.bind("<Enter>", Settings_on_enter)
        SettingsButton.bind("<Leave>", Settings_on_leave)
"""