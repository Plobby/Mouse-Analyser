
from tkinter import *
import tkinter as tk
import iomanager
from PIL import ImageTk, Image
counter = 0

def import_video():
   iomanager.get_videos(True)

def show_window():
    app = Pages()
    app.protocol("WM_DELETE_WINDOW", close_window)
    app.mainloop()

def close_window():
    #exits program
    raise SystemExit
#root = Tk() # TK has to be before the images however cant initialize images in pages if they're after the page, however required to be before Tk(), Toplevel() ect.

# Pages Code From = https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
class Pages(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #For loop that uses .grid to initialize frames
        for F in (VideoPage, DataPage, SettingsPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="news")

            #First page that shows - uses page name
        self.show_frame(VideoPage)
        #shows the frame from frame name
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        #Allows variables between the pages, requires self.controller = controller
    def get_page(self, page_class):
        return self.frames[page_class]

TitleLabelImage = ImageTk.PhotoImage(Image.open("../Assets/TitleBar.jpg"))
SettingsImage = ImageTk.PhotoImage(Image.open("../Assets/SettingsBar.jpg"))
SettingsHoverImage = ImageTk.PhotoImage(Image.open("../Assets/SettingsHover.jpg"))
VideoImage = ImageTk.PhotoImage(Image.open("../Assets/VideoBar.jpg"))
VideoHoverImage = ImageTk.PhotoImage(Image.open("../Assets/VideoHover.jpg"))
ExitImage = ImageTk.PhotoImage(Image.open("../Assets/ExitBar.jpg"))
ExitHoverImage = ImageTk.PhotoImage(Image.open("../Assets/ExitHover.jpg"))
SmthingImage = ImageTk.PhotoImage(Image.open("../Assets/DataBar.jpg"))

class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #
        self.controller=controller
        #Shows Title in Top Right
        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0).grid(row=0, column=1)
        #Shows Video Page Button m in Menu
        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0)
        VideoButton.grid(column=2, row=0)
        #Shows ???? Page Button in Menu
        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0)
        SmthingButton.grid(column=3, row=0)
        #Shows Settings Page Button in Menu
        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0)
        SettingsButton.grid(row=0, column=4)
        #Shows last item in Menu
        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,)
        ExitButton.grid(row=0, column=5)
        #Placeholder canvas for video playback
        VideoFrame = Canvas(self, width= 585, height = 445,bg="black").grid(row = 1,rowspan = 4, column = 2,columnspan= 5,padx=50,pady=50)
        #Import Video Function
        PlayVideoButton = Button(self, text="Import", command=import_video).grid(row=2, column = 1)

        #Creates an Hover Effect on the Menu Images - functions cannot be called outside of class due to "class" has no attribute "variable name"
class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Shows Title in Top Right
        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0).grid(row=0, column=1)
        #Shows Video Page Button m in Menu
        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0).grid(column=2, row=0)
        #Shows ???? Page Button in Menu
        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0).grid(column=3, row=0)
        #Shows Settings Page Button in Menu
        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0).grid(row=0, column=4)
        #Shows last item in Menu
        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,).grid(row=0, column=5)

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Shows Title in Top Right
        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0).grid(row=0, column=1)
        #Shows Video Page Button m in Menu
        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0).grid(column=2, row=0)
        #Shows ???? Page Button in Menu
        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0).grid(column=3, row=0)
        #Shows Settings Page Button in Menu
        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0).grid(row=0, column=4)
        #Shows last item in Menu
        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,).grid(row=0, column=5)



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