import tkinter as tk
import iomanager
import threading
from PIL import ImageTk, Image
import PIL
import cv2

# Load images
AddVideosImage = ImageTk.PhotoImage(Image.open("../Assets/AddVideosButton.jpg"))
ClearImage = ImageTk.PhotoImage(Image.open("../Assets/ClearButton.jpg"))
ProcessImage = ImageTk.PhotoImage(Image.open("../Assets/ProcessButton.jpg"))

image_title = ImageTk.PhotoImage(file="../Assets/TitleBarDark.png")

# Colour variables
color_background = "#202020"
color_hover = "#2B2B2B"
color_container = "#383838"
color_text = "#D4D4D4"

# Global variable to store app instance
app = None

# Function to import videos
def import_video():
    videos = iomanager.get_videos(True)
    first = iomanager.VideoInput(videos[0])
    app.play_video(first)

# Function to show the GUI
def show_window():
    global app
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
        tk.Toplevel.__init__(self, *args, **kwargs, bg=color_background)

        # Configure resizing options through grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Create contents
        self.add_toolbar()
        self.add_frames()
        self.add_statusbar()
        
        # Show the first frame
        self.show_frame(VideoPage)
    
    # Function to add the navigation bar
    def add_toolbar(self):
        # Frame for the title bar
        title_bar_frame = tk.Frame(self, bg=color_container)
        title_bar_frame.grid(row=0, column=0, sticky="nesw", pady=(0, 4))
        # Set expanding values
        title_bar_frame.grid_rowconfigure(0, weight=0)
        title_bar_frame.grid_columnconfigure(0, weight=0)
        title_bar_frame.grid_columnconfigure(1, weight=1)
        title_bar_frame.grid_columnconfigure(2, weight=0)
        # Shows Title in Top Right
        TitleLabel = tk.Label(title_bar_frame, image=image_title, bd=0, bg=color_container, highlightthickness=0)
        TitleLabel.grid(row=0, column=0, padx=10)
        # Expanding to fill space
        filler_frame = tk.Frame(title_bar_frame, bg=color_container)
        filler_frame.grid(row=0, column=1)
        # Frame for the buttons
        button_frame = tk.Frame(title_bar_frame, bg=color_container)
        button_frame.grid(row=0, column=2)
        # Shows Video Page Button in Menu
        VideoButton = MenuButton(button_frame, "Video", lambda: self.show_frame(VideoPage))
        VideoButton.grid(row=0, column=0, padx=4)
        # Shows Data Page Button in Menu
        SmthingButton = MenuButton(button_frame, "Data", lambda: self.show_frame(DataPage))
        SmthingButton.grid(row=0, column=1, padx=4)
        # Shows Settings Page Button in Menu
        SettingsButton = MenuButton(button_frame, "Settings", lambda: self.show_frame(SettingsPage))
        SettingsButton.grid(row=0, column=2, padx=4)
        # Shows Exit button in Menu
        ExitButton = MenuButton(button_frame, "Exit", close_window)
        ExitButton.grid(row=0, column=3, padx=4)

    # Function to add the frame view
    def add_frames(self):
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

    # Function to add the status bar
    def add_statusbar(self):
        # Frame for the status bar
        status_bar_frame = tk.Frame(self, bg=color_container)
        status_bar_frame.grid(row=2, column=0, sticky="nesw", pady=(4, 0))
        status_bar_frame.grid_columnconfigure(0, weight=1)
        status_bar_frame.grid_columnconfigure(1, weight=1)
        # Status bar text
        status_bar_text = tk.Label(status_bar_frame, text="Status: Ready to process.", bg=color_container, fg=color_text)
        status_bar_text.grid(row=0, column=0, sticky="nsw", pady=2, padx=10)
        # Copyright text
        copyright_text = tk.Label(status_bar_frame, text="Copyright: \xa9 MouseHUB 2020.", bg=color_container, fg=color_text)
        copyright_text.grid(row=0, column=1, sticky="nes", pady=2, padx=10)

    # Shows the frame from frame name
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Allows variables between the pages, requires self.controller = controller
    def get_page(self, page_class):
        return self.frames[page_class]

    # Function to play a video
    def play_video(self, video):
        video.open()
        self.playing = video
        self.play_video_frame()

    # Function to play a frame of a video then move onto the next frame
    def play_video_frame(self):
        frame = self.playing.get_frame()
        if (frame is None):
            self.playing = None
        else:
            self.set_video_render(frame)
            self.after(15, func = self.play_video_frame)

    # Function to set the video frame image
    def set_video_render(self, frame):
        canv = self.get_page(VideoPage).VideoFrame
        canv_width = canv.winfo_width()
        canv_height = canv.winfo_height()
        frame.thumbnail((canv_width, canv_height), Image.ANTIALIAS)
        frame = PIL.ImageTk.PhotoImage(image=frame)
        self.frame = frame
        canv.create_image(canv_width/2, canv_height/2, image=self.frame, anchor=tk.CENTER)

class VideoPage(tk.Frame):
    def __init__(self, parent, container):
        # Call superclass function
        tk.Frame.__init__(self, parent, bg=color_background)
        # Configure resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # Videos List
        queue_frame = tk.Frame(self, bg=color_container)
        queue_frame.grid(row=0, column=0, sticky="nesw")
        # Add buttons to queue list
        add_videos_button = tk.Button(queue_frame, image=AddVideosImage, command=import_video, bd=0, highlightthickness=0)
        add_videos_button.grid(row=0, column=0)
        clear_button = tk.Button(queue_frame, image=ClearImage, command=lambda: print("Clear pressed!"), bd=0, highlightthickness=0)
        clear_button.grid(row=0, column=1)
        process_button = tk.Button(queue_frame, image=ProcessImage, command=lambda: print("Process pressed!"), bd=0, highlightthickness=0)
        process_button.grid(row=0, column=2)
        # Canvas for video playback
        self.VideoFrame = tk.Canvas(self, bg="black", highlightbackground=color_container)
        self.VideoFrame.grid(row=0, column=1, padx=(4, 0), sticky="nesw")

class DataPage(tk.Frame):
    def __init__(self, parent, container):
        # Call superclass function
        tk.Frame.__init__(self, parent)

class SettingsPage(tk.Frame):
    def __init__(self, parent, container):
        # Call superclass function
        tk.Frame.__init__(self, parent)

class MenuButton(tk.Button):
    def __init__(self, parent, text, func):
        tk.Button.__init__(self, parent, text=text, command=func, bd=0, bg=color_container, fg=color_text, font=("Century Schoolbook Bold Italic", 18), padx=8, highlightthickness=0)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(bg=color_hover)

    def on_leave(self, event):
        self.configure(bg=color_container)