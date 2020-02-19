import tkinter as tk
import iomanager
from PIL import ImageTk, Image
import cv2 as cv2
import time
from threading import Timer
from queue import Queue, Empty

#color_background = "#202020"
#color_hover = "#2B2B2B"
#color_container = "#383838"
#color_text = "#D4D4D4"

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
        tk.Toplevel.__init__(self, *args, **kwargs)
        # Create new theme manager
        self.theme_manager = ThemeManager(self)
        self.theme_manager.register_item("bgr", self)
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
        # Apply the theme manager colours
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
        tk.Frame.__init__(self, parent)
        parent.app.theme_manager.register_item("bgr", self)
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
        queue_container = tk.Frame(self)
        queue_container.grid(row=0, column=0, sticky="nesw")
        queue_container.grid_rowconfigure(0, weight=0)
        queue_container.grid_rowconfigure(1, weight=1)
        queue_container.grid_columnconfigure(0, weight=1)
        parent.app.theme_manager.register_item("bgr", queue_container)
        # Queue buttons
        queue_buttons_frame = tk.Frame(queue_container)
        queue_buttons_frame.grid(row=0, column=0, sticky="nesw", pady=(0, 4))
        parent.app.theme_manager.register_item("ctr", queue_buttons_frame)
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
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nesw")
        parent.app.theme_manager.register_item("bgr", self)

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nesw")
        parent.app.theme_manager.register_item("bgr", self)
        # Configuring rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Bind parent
        self.app = parent.app

        # Creating a frame to put all the buttons in.
        settings_frame = tk.Frame(self)
        settings_frame.grid(row=0,column=1,sticky="nesw")
        parent.app.theme_manager.register_item("bgr", settings_frame)
        self.change_theme_button = tk.Button(settings_frame, text="Theme: Dark", command=self.rotate_theme)
        self.change_theme_button.config(font=("Century Schoolbook Bold Italic", 18), padx=8, highlightthickness=0)
        self.change_theme_button.grid(row=0,column=0,pady=4)
        parent.app.theme_manager.register_item("ctr", self.change_theme_button)
        parent.app.theme_manager.register_item("txt", self.change_theme_button)

        self.tkvar = tk.StringVar(load)

        # Dictionary with options
        choices = { 'Dark','Light','Debug'}
        self.tkvar.set('Dark') # set the default option
        # link function to change dropdown
        self.tkvar.trace('w', self.change_dropdown)

        popupMenu = tk.OptionMenu(self, self.tkvar, *choices)
        label = tk.Label(self, text="Choose a theme!")
        label.grid(row = 1, column = 1)
        parent.app.theme_manager.register_item("bgr", label)
        parent.app.theme_manager.register_item("txt", label)
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
    theme_manager = None

    def __init__(self, parent, text, func, theme_manager):
        # Load and store images
        self.tab = ImageTk.PhotoImage(file="../Assets/Tab.png")
        self.tab_active = ImageTk.PhotoImage(file="../Assets/TabActive.png")

        # Constructor call
        tk.Button.__init__(self, parent, image=self.tab, text=text, compound="center", command=func, bd=0, font=("Rockwell", 16), pady=0, highlightthickness=0)

        # Configure theme manager colours
        theme_manager.register_item("ctr", self)
        theme_manager.register_item("actr", self)
        theme_manager.register_item("txt", self)

        # Register events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        if (not self.active):
            self.configure(image=self.tab_active)

    def on_leave(self, event):
        if (not self.active):
            self.configure(image=self.tab)
    
    def set_active(self, state):
        self.active = state
        if (self.active):
            self.configure(image=self.tab_active)
        else:
            self.configure(image=self.tab)

class IconButton(tk.Button):
    def __init__(self, parent, image, func, theme_manager):
        tk.Button.__init__(self, parent, image=image, compound="left", command=func, bd=0, padx=8, highlightthickness=0)
        theme_manager.register_item("ctr", self)
        theme_manager.register_item("actr", self)
        self.image = image

# - VIDEO ITEMS
class VideoQueue(tk.Frame):
    videos = []

    def __init__(self, parent, theme_manager):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.scrollitems = tk.Frame(self)
        self.scrollitems.grid(row=0, column=0, sticky="nesw")
        theme_manager.register_item("ctr", self.scrollitems)
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
    controls_trackbar = None
    play_image = None
    play_image_hover = None
    pause_image = None
    pause_image_hover = None
    buffer = None

    drawn = 0

    # Constructor
    def __init__(self, parent, theme_manager):
        # Create read buffer
        self.buffer = Queue(maxsize=128)
        # Load images
        self.play_image = ImageTk.PhotoImage(file="../Assets/ButtonPlay.png")
        self.play_image_hover = ImageTk.PhotoImage(file="../Assets/ButtonPlayHover.png")
        self.pause_image = ImageTk.PhotoImage(file="../Assets/ButtonPause.png")
        self.pause_image_hover = ImageTk.PhotoImage(file="../Assets/ButtonPauseHover.png")
        # Call superclass constructor
        tk.Frame.__init__(self, parent)
        theme_manager.register_item("bgr", self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        # Create canvas
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.grid(row=0, column=0, sticky="nesw")
        theme_manager.register_item("actr", self.canvas)
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.canvas.bind("<Configure>", self.on_resize)
        # Create player bar
        self.controls_frame = tk.Frame(self)
        self.controls_frame.grid(row=1, column=0, sticky="nesw", padx=10, pady=8)
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_rowconfigure(0, weight=0)
        self.controls_frame.grid_rowconfigure(1, weight=0)
        theme_manager.register_item("bgr", self.controls_frame)
        self.controls_play = tk.Button(self.controls_frame, bd=0, image=self.play_image, command=self.toggle)
        self.controls_play.grid(row=0, column=0, sticky="ns")
        theme_manager.register_item("bgr", self.controls_play)
        theme_manager.register_item("abgr", self.controls_play)
        # Create player trackbar
        self.controls_trackbar = VideoTrackbar(self.controls_frame)
        self.controls_trackbar.grid(row=1, column=0, sticky="nesw")
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
            # Increment drawn count
            self.drawn += 1
            # Update trackbar progress
            # TODO: Run as daemonized thread
            self.controls_trackbar.update(self.drawn, self.source_input.frames_total)
        except:
            # Return - no frame found
            return

    # Function to handle frame resizing
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

class VideoTrackbar(tk.Canvas):
    # Variables
    current_frame = 0
    end_frame = 0
    percent = 0

    # Constructor
    def __init__(self, parent, theme_manager):
        # Call superclass constructor
        tk.Canvas.__init__(self, parent, highlightthickness=0, height=30)
        theme_manager.register_item("bgr", self)
        # Bind theme manager to object variable
        self.theme_manager = theme_manager
        # Initialize variables
        self.current_frame = 0
        self.end_frame = 0
        # Register resize listener
        self.bind('<Configure>', self._resize)

    # Update the current progress bar
    def update(self, current_frame, end_frame):
        # Update variables
        self.current_frame = current_frame
        self.end_frame = end_frame
        # Calculate percentage completion from frames
        if (self.current_frame >= 0 and self.end_frame > 0):
            self.percent = (self.current_frame / self.end_frame)
        # Call redraw function with new frames
        self.redraw()

    # Redraw the progress bar without new frames
    def redraw(self):
        # Check if the current frame and end frame are both zero - if so, no video is playing
        if (self.current_frame == 0 and self.end_frame == 0):
            # Draw full empty bar
            self.coords(self.bar_start, 5, 12, 5, 18)
            # Draw trackbar pointer
            self.coords(self.tracker_outer, 1, 8, 15, 22)
            self.coords(self.tracker_inner, 3, 10, 13, 20)
        else:
            # Calculate current point from percentage
            point = self.w * self.percent
            # Draw filled portion of bar
            self.coords(self.bar_start, 5, 12, point, 18)
            # Draw trackbar pointer
            self.coords(self.tracker_outer, point - 7, 8, point + 7, 22)
            self.coords(self.tracker_inner, point - 5, 10, point + 5, 20)

    # Function for when the canvas is resized
    def _resize(self, event):
        # Get the new width
        self.w = event.width - 10
        # Draw full empty bar
        self.bar_end = self.create_rectangle(5, 12, self.w, 18, fill="blue")
        self.bar_start = self.create_rectangle(5, 12, self.w, 18, fill="red")
        # Draw trackbar pointer
        self.tracker_outer = self.create_oval(1, 8, 15, 22, fill="orange")
        self.tracker_inner = self.create_oval(3, 10, 13, 20, fill="green")
        # TODO: Fill based on theme
        # Redraw the progress
        self.redraw()

# - APP ITEMS
class AppToolbar(tk.Frame):
    # Variables
    icon = None
    button_frame = None
    buttons = []
    parent = None

    # Images
    image_title = None

    # Constructor
    def __init__(self, parent):
        # Call superclass constructor
        tk.Frame.__init__(self, parent)
        # Bind parent for theme manager later
        self.parent = parent
        self.grid(row=0, column=0, sticky="nesw", pady=(0, 4))
        parent.theme_manager.register_item("ctr", self)
        # Load images
        self.image_title = ImageTk.PhotoImage(file="../Assets/TitleBarDark.png")
        # Set grid values
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Add title and spacing container
        self.icon = tk.Label(self, image=self.image_title, bd=0, highlightthickness=0)
        self.icon.grid(row=0, column=0, sticky="nsw")
        parent.theme_manager.register_item("ctr", self.icon)
        # Frame for the buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=1, padx=4, pady=(11, 0), sticky="es")
        parent.theme_manager.register_item("ctr", self.button_frame)

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
        btn = MenuButton(self.button_frame, text, lambda: self.button_click(btn, callback), parent.theme_manager)
        btn.grid(row=0, column=len(self.buttons), padx=4)
        self.parent.theme_manager.register_item("ctr", btn)
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
    def __init__(self, parent, theme_manager):
        tk.Frame.__init__(self, parent)
        theme_manager.register_item("ctr", self)
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
    def __init__(self, parent, copyright, theme_manager):
        # Frame for the status bar
        tk.Frame.__init__(self, parent)
        theme_manager.register_item("ctr", self)
        self.grid(row=2, column=0, sticky="nesw", pady=(4, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Status bar text
        self.status_label = tk.Label(self, text="Status: Ready to process.")
        theme_manager.register_item("ctr", self.status_label)
        theme_manager.register_item("txt", self.status_label)
        self.status_label.grid(row=0, column=0, sticky="nsw", pady=2, padx=10)
        # Copyright text
        label = tk.Label(self, text=copyright)
        theme_manager.register_item("ctr", label)
        theme_manager.register_item("txt", label)
        label.grid(row=0, column=1, sticky="nes", pady=2, padx=10)

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
    # Variables
    themes = []
    current_theme_index = 0
    current_theme = None
    items = {
        "bgr": [],
        "hvr": [],
        "ctr": [],
        "txt": [],
        "abgr": [],
        "actr": []
    }
    container = None

    # Constructor
    def __init__(self, container):
        # Load themes
        self.register_theme(Theme("Dark", "#202020", "#2B2B2B", "#383838", "#D4D4D4"))
        self.register_theme(Theme("Light", "#EDEDED", "#76CBE3", "#F5F5F5", "#009696"))
        self.register_theme(Theme("Debug", "#000FFF", "#00FF00", "#FFF100", "#FF0000"))

    # Register a theme
    def register_theme(self, theme):
        # Append the added theme
        self.themes.append(theme)

    # Function to register the item
    def register_item(self, objtype, obj):
        # Append the new item on the correct type
        self.items[objtype].append(obj)

    # Rotate to the next theme
    def rotate_theme(self):
        # Increment if not at the end of the themes list
        if (self.current_theme_index < (len(self.themes) - 1)):
            self.current_theme_index += 1
        else:
            self.current_theme_index = 0
        # Apply the new theme
        self.apply_theme(self.themes[self.current_theme_index])
        # Return the theme name
        return self.themes[self.current_theme_index]._name

    # Apply a theme
    def apply_theme(self, theme):
        # Update the current theme
        self.current_theme = theme
        # Iterate background items
        for item in self.items["bgr"]:
            item.configure(bg=theme._bgcolor)
        # Iterate container items
        for item in self.items["ctr"]:
            item.configure(bg=theme._cntrcolor)
        # Iterate text items
        for item in self.items["txt"]:
            item.configure(fg=theme._txtcolor)
        # Iterate active background items
        for item in self.items["abgr"]:
            item.configure(activebackground=theme._bgcolor)
        # Iterate active container items
        for item in self.items["actr"]:
            item.configure(activebackground=theme._cntrcolor)

    def apply_last_theme(self):
        # Get the last theme
        settings = self.get_last_theme()
        # Apply the last theme
        self.apply_theme(Theme(settings[0],settings[1],settings[2],settings[3],settings[4]))

    # Get the last used theme
    def get_last_theme(self):
        # Open the settings file
        settingsFile = open('../settings.txt', 'r+')
        # Create array to store settings
        settings = []
        # Iterate all lines in find and append the line without line ending
        for line in settingsFile:
            settings.append(line.strip('\n'))
        # Close the settings file
        settingsFile.close()
        # Return the compiled settings
        return settings