import tkinter as tk
from tkinter import filedialog
import iomanager
from PIL import ImageTk, Image
import configparser
import subprocess
import os
import cv2 as cv2
import time
from threading import Timer
from queue import Queue, Empty
import videoproc

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
    theme_manager = None

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
        if os.name == "nt":
            self.iconbitmap("../Assets/IconLarge.ico")
        else:
            self.iconbitmap("@../Assets/IconLarge.xbm")
        self.geometry("1280x720")
        self.minsize(780, 520)
        # Create frame view
        page_view = AppPageView(self)
        self.video_page = page_view.add_page(VideoPage)
        self.data_page = page_view.add_page(DataPage)
        self.settings_page = page_view.add_page(SettingsPage)
        # Create toolbar
        toolbar = AppToolbar(self)
        toolbar.add_button("Video", self.video_page.tkraise).set_active(True)
        toolbar.add_button("Data", self.data_page.tkraise)
        toolbar.add_button("Settings", self.settings_page.tkraise)
        toolbar.add_button("Exit", self.close)
        # Create status bar
        self.status_bar = AppStatusBar(self, "Copyright: \xa9 MouseHUB 2020.")
        # Show the first frame
        self.video_page.tkraise()
        # Create new theme manager
        self.theme_manager = ThemeManager(self)
        self.theme_manager.register_theme(Theme("Dark", "#202020", "#2B2B2B", "#383838", "#D4D4D4"))
        self.theme_manager.register_theme(Theme("Light", "#EDEDED", "#76CBE3", "#F5F5F5", "#009696"))
        self.theme_manager.register_theme(Theme("Debug", "#000FFF", "#00FF00", "#FFF100", "#FF0000"))
        self.theme_manager.apply_last_theme()
        # Register window close event
        self.protocol("WM_DELETE_WINDOW", self.close)
        # Start the main app loop
        self.mainloop()

    # Function to close the window
    def close(self):
        # Stop any video if playing
        if (self.video_page.video_player.playing):
            self.video_page.video_player.stop()
        # Destroy the tkinter window
        self.destroy()
        # Stop the application
        raise SystemExit

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
        button_add = ImageTk.PhotoImage(file="../Assets/ButtonAdd.png")
        button_clear = ImageTk.PhotoImage(file="../Assets/ButtonClear.png")
        button_process = ImageTk.PhotoImage(file="../Assets/ButtonProcess.png")
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
        IconButton(queue_buttons_frame, button_add, self.import_videos).grid(row=0, column=0, padx=4, pady=4)
        IconButton(queue_buttons_frame, button_clear, self.clear_videos).grid(row=0, column=1, padx=4, pady=4)
        IconButton(queue_buttons_frame, button_process, self.process_videos).grid(row=0, column=2, padx=4, pady=4)
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

    # Function to clear the user selected videos
    def clear_videos(self):
        self.video_queue.clear_videos()

    # Function to process the user selected videos
    def process_videos(self):
        videos = self.video_queue.get_videos()
        videoproc.processVideo(videos[0], doSaveVid=True)
        # TODO: Process videos here

class DataPage(tk.Frame):
    def __init__(self, parent):
        # Call superclass function
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid(row=0, column=0, sticky="nesw")

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid(row=0, column=0, sticky="nesw")
        #Configuring rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)


        Yes = ImageTk.PhotoImage(file="../Assets/ButtonYesGr.png")
        No = ImageTk.PhotoImage(file="../Assets/ButtonNoRed.png")
        Open = ImageTk.PhotoImage(file="../Assets/ButtonOpen.png")
        self.Open = Open
        Path = ImageTk.PhotoImage(file="../Assets/ButtonPath.png")
        self.Path = Path
        NoSelect = ImageTk.PhotoImage(file="../Assets/ButtonNoSelect.png")
        Select = ImageTk.PhotoImage(file="../Assets/ButtonSelect.png")
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        outputLocation = self.config.get('General', 'OutputPath')
        # Creating a frame to put all the buttons in.
        settings_frame = tk.Frame(self,bg=color_background)
        settings_frame.grid(row=0,column=1,sticky="nesw")

        #General Settings
        GeneralLabel = tk.Label(self, text="General Settings", bg=color_background, fg="White", font=("Rockwell",20)).grid(row=0,column=0,sticky="w",pady=10,padx=10)
        #Change Directory / Open Output Location
        self.OutputLocationLabel = tk.Label(self,text="Output Directory - " + outputLocation, bg=color_background, fg="White", font=("Rockwell",13))
        self.OutputLocationLabel.grid(row=1,column=0,sticky="w",padx=10)
        OutputButton = tk.Button(self, command=self.SetDirectory, image=Path, compound="left" ,bg=color_background, highlightbackground=color_background, highlightthickness=0, bd=0,activebackground=color_background)
        OutputButton.grid(row=2,column=0,sticky="w",padx=10)
        OpenButton = tk.Button(self, command=self.OpenPath, image=Open, compound="left" ,bg=color_background, highlightbackground=color_background, highlightthickness=0, bd=0,activebackground=color_background)
        OpenButton.grid(row=2,column=0,sticky="w",padx=120)

        ThemeLabel= tk.Label(self, text="Client Theme", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=3, column=0, sticky='w',padx=10,pady=10)
        self.ti = tk.IntVar()
        self.TB1 = RadioButton(self,"Light",NoSelect,Select,self.ThemeSave,self.ti,1)
        self.TB1.grid(row=4, column=0, sticky='w',padx=10)
        self.TB3 = RadioButton(self,"Dark",NoSelect,Select,self.ThemeSave,self.ti,2)
        self.TB3.grid(row=4, column=0, sticky='w', padx=110)
        self.TB4 = RadioButton(self,"Debug",NoSelect,Select,self.ThemeSave,self.ti,3)
        self.TB4.grid(row=4, column=0, sticky='w', padx=210)
        #Video Settings
        VideoLabel = tk.Label(self, text="Video Settings", bg=color_background, fg="White", font=("Rockwell",20)).grid(row=5,column=0,sticky="w",pady=10,padx=10)
        #SaveVideo - Yes/No
        SaveLabel= tk.Label(self, text="Generate Video File", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=6, column=0, sticky='w',padx=10,pady=10)
        self.SVB = tk.IntVar()
        self.LB1 = CheckButton(self,Yes,No,self.GenerateVideo, self.SVB)
        self.LB1.grid(row=7,column=0,sticky="w",padx=10)
        #Video Type RadioButton
        VideoTypeLabel = tk.Label(self, text="Video Type", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=8, column=0,sticky='w', padx=10,pady=10)
        self.v = tk.IntVar()
        self.LB2 = RadioButton(self,"Raw",NoSelect,Select,self.VideoType,self.v,1)
        self.LB2.grid(row=9, column=0, sticky='w',padx=10)
        self.LB3 = RadioButton(self,"Greyscale",NoSelect,Select,self.VideoType,self.v,2)
        self.LB3.grid(row=9, column=0, sticky='w', padx=110)
        self.LB4 = RadioButton(self,"Mouse",NoSelect,Select,self.VideoType,self.v,3)
        self.LB4.grid(row=9, column=0, sticky='w', padx=210)
        #Bounding Box - Yes/No
        BoundingBoxLabel = tk.Label(self, text="Bounding Box", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=10,column=0,sticky='w',padx=10,pady=10)
        self.BBI = tk.IntVar()
        self.LB5 = CheckButton(self, Yes,No,self.BoundingBox,self.BBI)
        self.LB5.grid(row=11, column=0, sticky="w", padx=10)
        BoundingBoxLabel = tk.Label(self, text="Playback Buffer Size", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=12,column=0,sticky='w',padx=10,pady=10)
        #Playback Buzzer Size RadioButton
        self.BS = tk.IntVar()
        self.LB6 = RadioButton(self,"16",NoSelect,Select,self.BufferSize,self.BS,1)
        self.LB6.grid(row=13, column=0,sticky="w",padx=10)
        self.LB7 = RadioButton(self,"32",NoSelect,Select,self.BufferSize,self.BS,2)
        self.LB7.grid(row=13, column=0,sticky="w",padx=110)
        self.LB8 = RadioButton(self,"64",NoSelect,Select,self.BufferSize,self.BS,3)
        self.LB8.grid(row=13, column=0,sticky="w",padx=210)
        self.LB9 = RadioButton(self,"128",NoSelect,Select,self.BufferSize,self.BS,4)
        self.LB9.grid(row=13, column=0,sticky="w",padx=310)
        #Data Settings
        Data = tk.Label(self, text="Data Settings", bg=color_background, fg="White", font=("Rockwell",20), pady=20).grid(row=0,column=1,sticky="w")
        #Mouse Tracking Setting - Yes/No
        MouseTrackingLabel = tk.Label(self, text="Mouse Position", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=1,column=1, sticky="w", pady=10)
        self.MTI = tk.IntVar()
        self.RB1 = CheckButton(self, Yes,No, self.MouseTracking,self.MTI)
        self.RB1.grid(row=2,column=1, sticky="w")
        #Pose Estimations /Mouse Behaviour
        MouseBehaviourLabel = tk.Label(self, text="Mouse Behaviour", bg=color_background, fg="White", font=("Rockwell",16)).grid(row=3,column=1, sticky="w",pady=10)
        self.MBI = tk.IntVar()
        self.RB2 = CheckButton(self, Yes,No, self.MouseBehaviour,self.MBI)
        self.RB2.grid(row=4,column=1, sticky="w")

        self.togglebuttons()



    # Set Saved Video Directory and Display Label
    def SetDirectory(self):
        outputLocation = filedialog.askdirectory()
        if outputLocation == "":
            print("error")
        else:
            config = configparser.ConfigParser()
            config.read("config.ini")
            config.set("General", "OutputPath", outputLocation)
            with open('config.ini', 'w') as f:
                config.write(f)
            self.OutputLocationLabel.config(text="Output Location: " + outputLocation)
    #Set the Generate Video config
    def GenerateVideo(self):
        self.config.read("config.ini")
        v = self.SVB.get()
        if v == 1:
            self.config.set("Video", "Generate_Video", "0")
        elif v == 0:
            self.config.set("Video", "Generate_Video", "1")
        with open('config.ini', 'w') as f:
            self.config.write(f)
    #Opens file path
    def OpenPath(self):
        self.config.read("config.ini")
        output = self.config.get("General", "OutputPath")
        subprocess.Popen(f'explorer {os.path.realpath(output)}')
    #Change config for Type of Video Generated
    def VideoType(self):
        v = self.v.get()
        if v == 1:
            self.config.read("config.ini")
            self.config.set("Video", "Video_Type", 'Raw')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if v == 2:
            self.config.read("config.ini")
            self.config.set("Video", "Video_Type", 'Greyscale')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if v == 3:
            self.config.read("config.ini")
            self.config.set("Video", "Video_Type", 'Mouse')
            with open('config.ini', 'w') as f:
                self.config.write(f)
    #Changes config for bounding box in Video to Yes
    def BoundingBox(self):
        self.config.read("config.ini")
        v = self.BBI.get()
        print(v)
        if v == 1:
            self.config.set("Video", "Bounding_Box", "0")
        elif v == 0:
            self.config.set("Video", "Bounding_Box", "1")
        with open('config.ini', 'w') as f:
            self.config.write(f)
    #Changes config for playback buffer size
    def BufferSize(self):
        bs = self.BS.get()
        if bs == 1:
            self.config.read("config.ini")
            self.config.set("Video", "Buffer_Size", '16')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if bs == 2:
            self.config.read("config.ini")
            self.config.set("Video", "Buffer_Size", '32')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if bs == 3:
            self.config.read("config.ini")
            self.config.set("Video", "Buffer_Size", '64')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if bs == 4:
            self.config.read("config.ini")
            self.config.set("Video", "Buffer_Size", '128')
            with open('config.ini', 'w') as f:
                self.config.write(f)
    #Changes config for mouse location tracking
    def MouseTracking(self):
        self.config.read("config.ini")
        v = self.MTI.get()
        if v == 1:
            self.config.set("Data", "Tracking_Data", "0")
        elif v == 0:
            self.config.set("Data", "Tracking_Data", "1")
        with open('config.ini', 'w') as f:
            self.config.write(f)
    #Changes config for post estimation
    def MouseBehaviour(self):
        self.config.read("config.ini")
        v = self.MBI.get()
        if v == 1:
            self.config.set("Data", "Behaviour_Data", "0")
        elif v == 0:
            self.config.set("Data", "Behaviour_Data", "1")
        with open('config.ini', 'w') as f:
            self.config.write(f)
    def ThemeSave(self):
        v = self.ti.get()
        if v == 1:
            self.config.read("config.ini")
            self.config.set("General", "Theme", 'Light')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if v == 2:
            self.config.read("config.ini")
            self.config.set("General", "Theme", 'Dark')
            with open('config.ini', 'w') as f:
                self.config.write(f)
        if v == 3:
            self.config.read("config.ini")
            self.config.set("General", "Theme", 'Debug')
            with open('config.ini', 'w') as f:
                self.config.write(f)
    def togglebuttons(self):
        outputLocation = self.config.get('General', 'OutputPath')
        print(os.path.exists(outputLocation))
        if not os.path.exists(outputLocation):
            self.config.set("General", "OutputPath", 'No Valid File Path Detected ')
            with open('config.ini', 'w') as f:
                self.config.write(f)
            self.OutputLocationLabel.config(text="Output Location: " + outputLocation)
        Variable = self.config.get('Video', 'video_type')
        if Variable == "Raw":
            self.LB2.select()
        if Variable == "Greyscale":
            self.LB3.select()
        if Variable == "Mouse":
            self.LB4.select()
        Variable = self.config.get('Video', 'Generate_Video')
        if Variable == '0':
            self.LB1.select()
        Variable = self.config.get('Data', 'tracking_data')
        if Variable == '0':
            self.RB1.select()
        Variable = self.config.get('Data', 'behaviour_data')
        if Variable == '0':
            self.RB2.select()
        Variable = self.config.get('Video', 'bounding_box')
        if Variable == '0':
            self.LB5.select()
        Variable = self.config.get('General', 'Theme')
        if Variable == "Light":
            self.TB1.select()
        if Variable == "Dark":
            self.TB3.select()
        if Variable == "Debug":
            self.TB4.select()
        Variable = self.config.get('Video', 'buffer_size')
        if Variable == "16":
            self.LB6.select()
        if Variable == "32":
            self.LB7.select()
        if Variable == "64":
            self.LB8.select()
        if Variable == "128":
            self.LB9.select()
# - BUTTON ITEMS
class MenuButton(tk.Button):
    active = False

    def __init__(self, parent, text, func):
        self.tab = ImageTk.PhotoImage(file="../Assets/Tab.png")
        self.tab_active = ImageTk.PhotoImage(file="../Assets/TabActive.png")
        tk.Button.__init__(self, parent, image=self.tab, text=text, compound="center", command=func, bd=0, bg=color_container, activebackground=color_container, fg=color_text, font=("Rockwell", 16), pady=0, highlightthickness=0)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        if (not self.active):
            self.configure(image=self.tab_active)

    def on_leave(self, event):
        if (not self.active):
            self.configure(image=self.tab)
    
    def reConfigure(self, newBG, newFontColor):
        self.config(bg=newBG, fg=newFontColor)
    
    def set_active(self, state):
        self.active = state
        if (self.active):
            self.configure(image=self.tab_active)
        else:
            self.configure(image=self.tab)

class IconButton(tk.Button):
    def __init__(self, parent, image, func):
        tk.Button.__init__(self, parent, image=image, compound="left", command=func, bd=0, bg=color_container, activebackground=color_container, padx=8, highlightthickness=0)
        self.image = image

class CheckButton(tk.Checkbutton):
    def __init__(self,parent,image,image1,func,var):
        tk.Checkbutton.__init__(self,parent,image=image,variable=var,selectimage=image1, compound="left", command=func, bd=0, bg=color_background,selectcolor=color_background, activebackground=color_background,highlightbackground=color_background, highlightthickness=0, indicatoron=0)
        self.image = image
        self.image1 = image1
class RadioButton(tk.Radiobutton):
    def __init__(self,parent,text,image,image1,func,var,value):
        tk.Radiobutton.__init__(self,parent,text=text,image=image,selectimage=image1,compound="center", variable=var,command=func,value=value, bd=0, bg=color_background,selectcolor=color_background, activebackground=color_background,highlightbackground=color_background, fg="white", font=("Rockwell", 14), pady=0, highlightthickness=0,indicatoron=0)
        self.image = image
        self.image1 = image1
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
    controls_frame = None
    controls_play = None
    play_image = None
    play_image_hover = None
    pause_image = None
    pause_image_hover = None

    buffer = None

    # Constructor
    def __init__(self, parent):
        # Create read buffer
        self.buffer = Queue(maxsize=128)
        # Load images
        self.play_image = ImageTk.PhotoImage(file="../Assets/ButtonPlay.png")
        self.play_image_hover = ImageTk.PhotoImage(file="../Assets/ButtonPlayHover.png")
        self.pause_image = ImageTk.PhotoImage(file="../Assets/ButtonPause.png")
        self.pause_image_hover = ImageTk.PhotoImage(file="../Assets/ButtonPauseHover.png")
        # Call superclass constructor
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        # Create canvas
        self.canvas = tk.Canvas(self, bg="black", highlightbackground=color_container)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.canvas.bind("<Configure>", self.on_resize)
        # Create player bar
        self.controls_frame = tk.Frame(self, bg=color_background)
        self.controls_frame.grid(row=1, column=0, sticky="nesw", padx=10, pady=8)
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_play = tk.Button(self.controls_frame, bd=0, bg=color_background, activebackground=color_background, image=self.play_image, command=self.toggle)
        self.controls_play.grid(row=0, column=0, sticky="ns")
        # Bind hover events
        self.controls_play.bind("<Enter>", self.play_hover)
        self.controls_play.bind("<Leave>", self.play_leave)

    # Function for when the mouse starts hovering the play button
    def play_hover(self, event):
        # Check if the video is playing
        if (self.playing):
            self.controls_play.configure(image=self.pause_image_hover)
        else:
            self.controls_play.configure(image=self.play_image_hover)

    # Function for when the mouse stops hovering the play button
    def play_leave(self, event):
        # Check if the video is playing
        if (self.playing):
            self.controls_play.configure(image=self.pause_image)
        else:
            self.controls_play.configure(image=self.play_image)

    # Function to set the video source
    def set_source(self, video):
        self.source = video

    # Function to clear the video source
    def clear_source(self):
        self.source = None
        self.source_input.close()
        self.source_input = None

    # Function to toggle the video playing state
    def toggle(self):
        # Check a source is present
        if (not self.source is None):
            # Check if playing
            if (self.playing):
                # Stop playing
                self.pause()
                # Update button state
                self.controls_play.configure(image=self.pause_image_hover)
            else:
                # Start playing
                self.play()
                # Update button state
                self.controls_play.configure(image=self.play_image_hover)

    # Function to play the video
    def play(self):
        # Check a source is present
        if (not self.source is None):
            # Mark as playing
            self.playing = True
            # Create input stream
            if (self.source_input is None):
                self.source_input = iomanager.VideoInput(self.source)
            # Start reading frames
            self.source_input.start(self.buffer)
            # Run timer to play frames
            timer = Timer(interval=self.source_input.frames_interval, function=self._draw_frame, args=[self.buffer])
            timer.daemon = True
            timer.start()

    # Function to pause the video
    def pause(self):
        # Check a source is present
        if (not self.source is None and not self.source_input is None):
            self.playing = False
            self.source_input.stop()

    # Function to stop the video
    def stop(self):
        # Check a source is present
        if (not self.source is None and not self.source_input is None):
            self.playing = False
            self.source = None
            self.source_input = None

    # Function to draw a frame
    def _draw_frame(self, target):
        # Return if not playing
        if (not self.playing):
            return
        # Get the next frame
        try:
            # Call next frame draw
            timer = Timer(interval=self.source_input.frames_interval, function=self._draw_frame, args=[self.buffer])
            timer.daemon = True
            timer.start()
            # Get the frame
            frame = target.get(block=False)
            # Process the frame and resize correctly
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #cv2.putText(frame, "Queue Size: {}".format(target.qsize()), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            frame = Image.fromarray(frame)
            frame.thumbnail((self.width, self.height), Image.ANTIALIAS)
            frame = ImageTk.PhotoImage(image=frame)
            # Draw the image
            self.canvas.create_image(self.width/2, self.height/2, image=frame, anchor=tk.CENTER)
            self.frame = frame
        except:
            # Return - no frame found
            return

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
        tk.Label(self, image=self.image_title, bd=0, bg=color_container, highlightthickness=0).grid(row=0, column=0, sticky="nsw")
        # Frame for the buttons
        self.button_frame = tk.Frame(self, bg=color_container)
        self.button_frame.grid(row=0, column=1, padx=4, pady=(11, 0), sticky="es")

    # Function for when a button is clicked
    def button_click(self, item, callback):
        # Change active button
        for btn in self.buttons:
            if (btn == item):
                btn.set_active(True)
            else:
                btn.set_active(False)
        # Call button callback function
        callback()

    # Function to add a button to the toolbar
    def add_button(self, text, callback):
        btn = MenuButton(self.button_frame, text, lambda: self.button_click(btn, callback))
        btn.grid(row=0, column=len(self.buttons), padx=4)
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
        # Assign parent
        self.app = parent

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

# - THEME ITEMS
class Theme:
    def __init__(self, name, bgcolor, hvrcolor, cntrcolor, txtcolor):
        self._name = name
        self._bgcolor = bgcolor
        self._hvrcolor = hvrcolor
        self._cntrcolor = cntrcolor
        self._txtcolor = txtcolor

    def title(self):
        return self._name

    def background(self):
        return self._bgcolor

    def hover(self):
        return self._hvrcolor

    def container(self):
        return self._cntrcolor

    def text(self):
        return self._txtcolor

    def change_theme(self, name, bgcolor, hvrcolor, cntrcolor, txtcolor):
        self.__init__(name, bgcolor, hvrcolor, cntrcolor, txtcolor)

class ThemeManager:
    themes = []
    current_theme_index = 0
    current_theme = None
    container = None

    def __init__(self, container):
        self.themes = []
        self.current_theme_index = 0
        self.container = container

    def register_theme(self, theme):
        self.themes.append(theme)

    def rotate_theme(self):
        if (self.current_theme_index < (len(self.themes) - 1)):
            self.current_theme_index += 1
        else:
            self.current_theme_index = 0
        self.apply_theme(self.themes[self.current_theme_index])
        return self.themes[self.current_theme_index]._name

    def apply_theme(self, theme):
        # For every widget in the parent (aka the whole interface)...
        for widget in self.container.winfo_children():
            widget.configure(bg=theme._bgcolor)
            #widget.configure(fg=themeTextDict[self.themeList[currentThemeIndex]])
            widget.configure()
            if (type(widget)==MenuButton):
                print("MenuButton found!")
                #widget.reConfigure(themeBackDict[self.themeList[currentThemeIndex]],themeTextDict[self.themeList[currentThemeIndex]])
            if (type(widget)==tk.Frame):
                widget.configure(bg=theme._cntrcolor)

    def apply_last_theme(self):
        settings = self.get_last_theme()
        self.apply_theme(Theme(settings[0],settings[1],settings[2],settings[3],settings[4]))

    # Open the settings file and load the last used/default theme.
    def get_last_theme(self):
        settingsFile = open('../settings.txt', 'r+')
        settings = []
        line = ""
        for line in settingsFile:
            settings.append(line.strip('\n'))
        settingsFile.close()
        return settings