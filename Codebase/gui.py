
from tkinter import *
import tkinter as tk
import iomanager
from PIL import ImageTk, Image
counter = 0

def import_video():
   iomanager.get_videos(True)


def close_window():
    raise SystemExit

def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

LARGE_FONT= ("Verdana", 12)

root = Tk()
TitleLabelImage = ImageTk.PhotoImage(Image.open("Assets/TitleBar.jpg"))
SettingsImage = ImageTk.PhotoImage(Image.open("Assets/SettingsBar.jpg"))
SettingsHoverImage = ImageTk.PhotoImage(Image.open("Assets/SettingsHover.jpg"))
VideoImage = ImageTk.PhotoImage(Image.open("Assets/VideoBar.jpg"))
VideoHoverImage = ImageTk.PhotoImage(Image.open("Assets/VideoHover.jpg"))
ExitImage = ImageTk.PhotoImage(Image.open("Assets/ExitBar.jpg"))
ExitHoverImage = ImageTk.PhotoImage(Image.open("Assets/ExitHover.jpg"))
SmthingImage = ImageTk.PhotoImage(Image.open("Assets/DataBar.jpg"))

class Pages(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, VideoPage, DataPage, SettingsPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="news")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0)
        TitleLabel.grid(row=0, column=1)

        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0)
        VideoButton.grid(column=2, row=0)

        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0)
        SmthingButton.grid(column=3, row=0)

        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0)
        SettingsButton.grid(row=0, column=4)

        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,)
        ExitButton.grid(row=0, column=5)


class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0)
        TitleLabel.grid(row=0, column=1)

        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0)
        VideoButton.grid(column=2, row=0)

        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0)
        SmthingButton.grid(column=3, row=0)

        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0)
        SettingsButton.grid(row=0, column=4)

        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,)
        ExitButton.grid(row=0, column=5)

        VideoFrame = Canvas(self, width= 585, height = 445,bg="black").grid(row = 1,rowspan = 4, column = 2,columnspan= 5,padx=50,pady=50)


        PlayVideoButton = Button(self, text="play", command=import_video).grid(row=2, column = 1)

        def Exit_on_enter(e):
            VideoPage.ExitButton['image'] = ExitHoverImage
        def Exit_on_leave(e):
            ExitButton['image'] = ExitImage
        ExitButton.bind("<Enter>", Exit_on_enter)
        ExitButton.bind("<Leave>", Exit_on_leave)

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
class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0)
        TitleLabel.grid(row=0, column=1)

        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0)
        VideoButton.grid(column=2, row=0)

        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0)
        SmthingButton.grid(column=3, row=0)

        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0)
        SettingsButton.grid(row=0, column=4)

        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,)
        ExitButton.grid(row=0, column=5)



class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        TitleLabel = Label(self, image=TitleLabelImage,width=500,height=175, bd=0, highlightthickness=0)
        TitleLabel.grid(row=0, column=1)

        VideoButton = Button(self, image=VideoImage,command=lambda: controller.show_frame(VideoPage),width=195,height=175, bd=0, highlightthickness=0)
        VideoButton.grid(column=2, row=0)

        SmthingButton = Button(self, image=SmthingImage,command=lambda: controller.show_frame(DataPage),width=195,height=175, bd=0, highlightthickness=0)
        SmthingButton.grid(column=3, row=0)

        SettingsButton = Button(self, image=SettingsImage,command=lambda: controller.show_frame(SettingsPage),width=195,height=175,bd=0, highlightthickness=0)
        SettingsButton.grid(row=0, column=4)

        ExitButton = Button(self, image=ExitImage, command = close_window,width=195,height=175,bd=0, highlightthickness=0,)
        ExitButton.grid(row=0, column=5)


app = Pages()
app.mainloop()
