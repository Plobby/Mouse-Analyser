import tkinter as tk
import iomanager
from PIL import ImageTk, Image
import PIL
import cv2
import time
from threading import Thread
from scheduler import Scheduler

# Colour variables
color_background = "#202020"
color_hover = "#2B2B2B"
color_container = "#383838"
color_text = "#D4D4D4"

# Load a tk window and widthdraw to allow images to be loaded
load = tk.Tk()
load.withdraw()

# Global variable to store app instance
app = None

# Function to show the GUI
def show_window():
    # Create a new app instance
    global app
    app = App()

# - APP ITEMS
class App(tk.Tk):
    # Variables
    video_page = None
    data_page = None
    settings_page = None
    status_bar = None

    # Constructor
    def __init__(self, *args, **kwargs):
        # Call superclass function
        tk.Toplevel.__init__(self, *args, **kwargs, bg=color_background)
        # Configure resizing options through grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        # Configure appearance
        self.title("MouseHUB")
        self.geometry("1280x720")
        self.minsize(720, 520)
        # Create frame view
        page_view = AppPageView(self)
        self.video_page = page_view.add_page(VideoPage)
        self.data_page = page_view.add_page(DataPage)
        self.settings_page = page_view.add_page(SettingsPage)
        # Create toolbar
        toolbar = AppToolbar(self)
        toolbar.add_button("Video", self.video_page.tkraise)
        toolbar.add_button("Data", self.data_page.tkraise)
        toolbar.add_button("Settings", self.settings_page.tkraise)
        toolbar.add_button("Exit", self.close)
        # Create status bar
        self.status_bar = AppStatusBar(self, "Copyright: \xa9 MouseHUB 2020.")
        # Show the first frame
        self.video_page.tkraise()
        # Register window close event
        self.protocol("WM_DELETE_WINDOW", self.close)
        # Start the main app loop
        self.mainloop()
    
    # Function to close the window
    def close(self):
        # Stop any video if playing
        if (self.video_page.video_player.playing):
            self.video_page.video_player.pause()
        # Destroy the tkinter window
        self.destroy()
        # Stop the application
        raise SystemExit

    # Function to play a frame of a video then move onto the next frame
    def play_video_frame(self):
        frame = self.playing_video.get_frame()
        if ((not frame is None) and self.playing):
            self.set_video_render(frame)
            self.set_status("Playing \"" + self.playing_video.file + "\": " + self.playing_video.get_progress())
            self.playing_timer = threading.Timer(self.playing_video.get_frame_interval(), self.play_video_frame)
            self.playing_timer.start()

# - PAGE ITEMS
class VideoPage(tk.Frame):
    # Variables
    video_queue = None

    # Constructor
    def __init__(self, parent):
        # Call superclass function
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid(row=0, column=0, sticky="nesw")
        # Load images
        icon_add = ImageTk.PhotoImage(file="../Assets/IconAdd.png")
        icon_add_active = ImageTk.PhotoImage(file="../Assets/IconAddActive.png")
        icon_delete = ImageTk.PhotoImage(file="../Assets/IconDelete.png")
        icon_delete_active = ImageTk.PhotoImage(file="../Assets/IconDeleteActive.png")
        icon_process = ImageTk.PhotoImage(file="../Assets/IconProcess.png")
        icon_process_active = ImageTk.PhotoImage(file="../Assets/IconProcessActive.png")
        # Configure resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # Videos List
        queue_container = tk.Frame(self, bg=color_background)
        queue_container.grid(row=0, column=0, sticky="nesw")
        queue_container.grid_rowconfigure(0, weight=0)
        queue_container.grid_rowconfigure(1, weight=1)
        queue_container.grid_columnconfigure(0, weight=1)
        # Queue buttons
        queue_buttons_frame = tk.Frame(queue_container, bg=color_container)
        queue_buttons_frame.grid(row=0, column=0, sticky="nesw", pady=(0, 4))
        # Add buttons
        IconButton(queue_buttons_frame, "Add", icon_add, icon_add_active, self.import_videos).grid(row=0, column=0, padx=4, pady=4)
        IconButton(queue_buttons_frame, "Clear", icon_delete, icon_delete_active, lambda: print("Clear pressed!")).grid(row=0, column=1, padx=4, pady=4)
        IconButton(queue_buttons_frame, "Process", icon_process, icon_process_active, lambda: print("Process pressed!")).grid(row=0, column=2, padx=4, pady=4)
        # Queue items list
        self.video_queue = VideoQueue(queue_container)
        self.video_queue.grid(row=1, column=0, sticky="nesw")
        # Video player
        self.video_player = VideoPlayer(self)
        self.video_player.grid(row=0, column=1, padx=(4, 0), sticky="nesw")
    
    # Function to allow the user to select and import videos
    def import_videos(self):
        videos = iomanager.get_videos(True)
        self.video_queue.add_videos(videos)
        if (len(videos) > 0):
            self.video_player.set_source(videos[0])
            self.video_player.play()

class DataPage(tk.Frame):
    def __init__(self, parent):
        # Call superclass function
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nesw")

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        # Call superclass function
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nesw")

# - BUTTON ITEMS
class MenuButton(tk.Button):
    def __init__(self, parent, text, func):
        tk.Button.__init__(self, parent, text=text, command=func, bd=0, bg=color_container, fg=color_text, font=("Century Schoolbook Bold Italic", 18), padx=8, highlightthickness=0)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(bg=color_hover)

    def on_leave(self, event):
        self.configure(bg=color_container)

class IconButton(tk.Button):
    def __init__(self, parent, text, image, image_active, func):
        tk.Button.__init__(self, parent, text=text, image=image, compound="left", command=func, bd=0, bg=color_container, fg=color_text, font=("Century Schoolbook Bold Italic", 14), padx=8, highlightthickness=0)
        self.image = image
        self.image_active = image_active
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(bg=color_hover, image=self.image_active)

    def on_leave(self, event):
        self.configure(bg=color_container, image=self.image)

# - VIDEO ITEMS
class VideoQueue(tk.Frame):
    videos = []

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.scrollitems = tk.Frame(self, bg=color_hover)
        self.scrollitems.grid(row=0, column=0, sticky="nesw")
        self.scrollitems.grid_columnconfigure(0, weight=1)
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.scrollbar.grid(row=0, column=1, sticky="nesw")

    def add_videos(self, videos):
        for video in videos:
            self.add_video(video)

    def add_video(self, video):
        self.videos.append(video)
        # TODO: Add video render here

    def remove_video(self, video):
        self.videos.remove(video)
        # TODO: Remove video render here
    
    def clear_videos(self):
        self.videos = []
        # TODO: Remove all video renders here

    def get_videos(self):
        return self.videos

class VideoPlayer(tk.Frame):
    # Variables
    width = None
    height = None
    canvas = None
    source = None
    source_input = None
    frame = None
    playing = False
    scheduler = None

    # Constructor
    def __init__(self, parent):
        # Call superclass constructor
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Create canvas
        self.canvas = tk.Canvas(self, bg="black", highlightbackground=color_container)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.canvas.bind("<Configure>", self.on_resize)

    # Function to set the video source
    def set_source(self, video):
        self.source = video

    # Function to clear the video source
    def clear_source(self):
        self.source = None
        #TODO: Close source correctly here
        self.source_input = None

    # Function to play the video
    def play(self):
        # Check a source is present
        if (not self.source is None):
            # Mark as playing
            self.playing = True
            # Create input stream
            self.source_input = iomanager.VideoInput(self.source)
            self.source_input.start()
            # Run a new scheduler
            time.sleep(0.05)
            self.scheduler = Scheduler(self.source_input.frames_interval, self._draw_frame)
            self.scheduler.start()

    # Function to pause the video
    def pause(self):
        # Check a source is present
        if (not self.source is None and not self.source_input is None):
            self.playing = False

    # Function to draw a frame
    def _draw_frame(self):
        # Return if no frame is ready to be read
        if (not self.source_input.can_read()):
            return
        # Get the next frame
        frame = self.source_input.read()
        # Process the frame and resize correctly
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame, "Queue Size: {}".format(self.source_input.queue.qsize()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        frame = PIL.Image.fromarray(frame)
        frame.thumbnail((self.width, self.height), Image.ANTIALIAS)
        frame = PIL.ImageTk.PhotoImage(image=frame)
        #self.canvas.after(0, lambda: self.canvas.configure(image=self.frame))
        #self.canvas.configure(image=self.frame)
        self.canvas.create_image(self.width/2, self.height/2, image=frame, anchor=tk.CENTER)
        self.frame = frame

    # Function to handle frame resizing
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

# - APP ITEMS
class AppToolbar(tk.Frame):
    # Variables
    button_frame = None
    buttons = []

    # Images
    image_title = None

    # Constructor
    def __init__(self, parent):
        # Call superclass constructor
        tk.Frame.__init__(self, parent, bg=color_container)
        self.grid(row=0, column=0, sticky="nesw", pady=(0, 4))
        # Load images
        self.image_title = ImageTk.PhotoImage(file="../Assets/TitleBarDark.png")
        # Set grid values
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Add title and spacing container
        tk.Label(self, image=self.image_title, bd=0, bg=color_container, highlightthickness=0).grid(row=0, column=0, padx=10, sticky="nsw")
        # Frame for the buttons
        self.button_frame = tk.Frame(self, bg=color_container)
        self.button_frame.grid(row=0, column=1, padx=4, pady=11, sticky="e")

    # Function to add a button to the toolbar
    def add_button(self, text, callback):
        btn = MenuButton(self.button_frame, text, callback).grid(row=0, column=len(self.buttons), padx=4)
        self.buttons.append(btn)
        return btn

    # Function to remove a button from the toolbar
    def remove_button(self, btn):
        self.buttons.remove(btn)
        btn.destroy()
        for i in range(0, len(self.buttons)):
            self.buttons[i].grid(row=0, column=i)

class AppPageView(tk.Frame):
    # Variables
    frames = []

    # Constructor
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=color_container)
        # Set grid values
        self.grid(column=0, row=1, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    # Function to add a page to the view
    def add_page(self, pagetype):
        page = pagetype(self)
        self.frames.append(page)
        return page

class AppStatusBar(tk.Frame):
    # Variables
    status_label = None
    status = "Ready to process."

    # Constructor
    def __init__(self, parent, copyright):
        # Frame for the status bar
        tk.Frame.__init__(self, parent, bg=color_container)
        self.grid(row=2, column=0, sticky="nesw", pady=(4, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Status bar text
        self.status_label = tk.Label(self, text="Status: Ready to process.", bg=color_container, fg=color_text)
        self.status_label.grid(row=0, column=0, sticky="nsw", pady=2, padx=10)
        # Copyright text
        tk.Label(self, text=copyright, bg=color_container, fg=color_text).grid(row=0, column=1, sticky="nes", pady=2, padx=10)
    
    # Function to update the status
    def set_status(self, status):
        self.status_label.configure(text="Status: " + str(status))
        self.status = status

    # Function to get the status
    def get_status(self):
        return self.status