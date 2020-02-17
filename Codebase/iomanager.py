from tkinter import filedialog
from tkinter import Tk
import tkinter as tk
from PIL import ImageTk, Image
import PIL
import numpy
import cv2
import gui
import cli_logger
from cli_logger import LogLevel
import Segmentation
import CCL

# Hide the main tkinter window
ROOT = Tk()
ROOT.withdraw()

# Create variable with allowed file types
VALID_FILES = [("mpeg videos", "*.mpg"), ("mp4 videos", "*.mp4"), ("avi videos", "*.avi")]

# Function to import videos
def get_videos(multiple):
    # Prompt for a file to be selected
    cli_logger.log(LogLevel.INFO, "Please select a file to analyse!")
    # Create variable to store videos
    videos = []
    # Check if multiple are allowed
    if multiple:
        # Inform the user multiple files are allowed
        cli_logger.log(LogLevel.INFO, "Multiple files can be selected!")
        # Select multiple files and return the result
        videos = filedialog.askopenfilenames(filetypes=VALID_FILES)
    else:
        # Select one file and return the result
        videos = [filedialog.askopenfilename(filetypes=VALID_FILES)]
    # Open the videos and return
    return videos

#Function to save a *LIST* of CV2 VideoCapture objects
def save_videos(videoCaps, outputLocation):
    if outputLocation == None: #This is for GUI mode, where a directory is not already given
        #Open folder selection dialog box
        outputLocation = filedialog.askdirectory()

    # Index for giving unique names to each video being saved
    fileIndex = 1

    for video in videoCaps:
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) #Get frame width
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Get frame height
        fps = int(video.get(cv2.CAP_PROP_FPS)) #Get video fps
        fourcc = int(cv2.VideoWriter_fourcc(*'mpg1')) #Fourcc code for writing .mpg video files

        #Concatenate outputLocation with output--fileIndex--.mpg
        fileLocation = outputLocation + "/output" + str(fileIndex) + ".mpg"
        #Create VideoWriter object using specs of the video being saved
        out = cv2.VideoWriter(fileLocation, fourcc, fps, (width, height))

        #Set frame position to the first frame of the video
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #Iterate while video is open
        while (video.isOpened()):
            #Read the next return and get the frame
            ret, frame = video.read()
            #Break if no frame is returned
            if (not ret):
                break

            #Write frame
            out.write(frame)

        #Release VideoCapture object
        video.release()
        #Release VideoWriter object
        out.release()

        fileIndex += 1

class VideoInput():
    frames_done = 0
    frames_total = 0
    progress = 0

    def __init__(self, file):
        self.file = file
    
    def open(self):
        self.cap = cv2.VideoCapture(self.file)
        self.frames_total = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def close(self):
        self.cap.release()
    
    def get_frame(self):
        if (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if (not ret):
                self.close()
                return None
            # TODO: Process the frame properly here
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = Segmentation.thresholdSegment(frame, Segmentation.otsuThreshold(frame))
            frame = PIL.Image.fromarray(frame)
            self.frames_done = self.frames_done + 1
            return frame
        self.close()
        return None
