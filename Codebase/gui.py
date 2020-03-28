import tkinter as tk
import iomanager
import numpy
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from PIL import ImageTk, Image
import cv2 as cv2
import time
from threading import Timer
from queue import Queue, Empty
import graphing as graph # Import graphing under name graph

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
        self.iconbitmap("../Assets/IconLarge.ico")
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
        # TODO: Process videos here

class DataPage(tk.Frame):
    def __init__(self, parent):
        # Call superclass function
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid(row=0, column=0, sticky="nesw")

        graphFigure = plt.figure(facecolor=color_background) # Figure for graphing.
        graphGenerator = graph.dataGraph() # object to store datagraph in.

        xLabels = {"Sleeping":0,"Eating":1,"Moving":2,"Undefined":3}
        yValues = [50,30,120,25]
        mouseReport = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,3,3,3,3,3,3,3,3,3,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2]

        xLabels2 = [5,6,7,8,5,6]
        yValues2 = [4,5,6,7,8,3]

        graphFigure, self.myPlot = graphGenerator.createBasicBarChart(graphFigure, [5,6,7,8], [4,5,6,7])
        #graphFigure, myPlot = graphGenerator.createStackedBarChart(graphFigure,1,5,xLabels,mouseReport)

        titleEntry = tk.Entry(self, bg = color_container, fg = color_text)
        titleEntry.grid(row = 2, column = 2, sticky = "nesw", padx = 50, pady = 5)
        setButton = tk.Button(self,bg = color_container, fg = color_text, text = "Set Title", command = lambda:self.getAndSetTitle(titleEntry,self.myPlot))
        setButton.grid(row = 2, column = 3, sticky = "nesw", padx = 5, pady = 5)


        self.myPlot.set_facecolor(color_background)
        self.myPlot.tick_params(labelcolor=color_text, color=color_container)
        for spine in self.myPlot.spines.values():
            spine.set_edgecolor(color_container)

        self.myPlot.set_xlabel("Time (s)", color = color_text)
        self.myPlot.set_ylabel("Activity per Division", color =  color_text)

        canvas1 = FigureCanvasTkAgg(graphFigure, self)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row = 3, column = 2, rowspan = 99)


    def showBarChart(self,graphFigure,graphGenerator,canvas1):
        # Code to implement graph on canvas + page

        canvas1.draw()
        canvas1.get_tk_widget().grid(row = 3, column = 2, rowspan = 99)

    def getAndSetTitle(self, titleEntry, myPlot):
        title = titleEntry.get()
        print(title)
        myPlot.set_title(title, color = color_text)



class SettingsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=color_background)
        self.grid(row=0, column=0, sticky="nesw")
        # Configuring rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Bind parent
        self.app = parent.app

        # Creating a frame to put all the buttons in.
        settings_frame = tk.Frame(self,bg=color_background)
        settings_frame.grid(row=0,column=1,sticky="nesw")
        self.change_theme_button = tk.Button(settings_frame, text="Theme: Dark", command=self.rotate_theme)
        self.change_theme_button.config(bg=color_container, fg=color_text,font=("Century Schoolbook Bold Italic", 18), padx=8, highlightthickness=0)
        self.change_theme_button.grid(row=0,column=0,pady=4)

        self.tkvar = tk.StringVar(load)

        # Dictionary with options
        choices = { 'Dark','Light','Debug'}
        self.tkvar.set('Dark') # set the default option
        # link function to change dropdown
        self.tkvar.trace('w', self.change_dropdown)

        popupMenu = tk.OptionMenu(self, self.tkvar, *choices)
        tk.Label(self,bg=color_background, fg=color_text, text="Choose a theme!").grid(row = 1, column = 1)
        popupMenu.grid(row = 2, column =1)

    def rotate_theme(self):
        name = self.app.theme_manager.rotate_theme()
        self.change_theme_button.config(text="Theme: " + name)

    # on change dropdown value
    def change_dropdown(self, *args):
        print(self.tkvar.get())

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
