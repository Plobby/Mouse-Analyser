from tkinter import filedialog
from PIL import Image
import PIL
import cv2
import gui
import cli_logger
from cli_logger import LogLevel
from queue import Queue
from threading import Thread
import time

# Variables
valid_files = [("Video Files", ("*.mp4", "*.mpg", "*.avi")), ("MP4 Videos", "*.mp4"), ("MPEG Videos", "*.mpg"), ("AVI Videos", "*.avi")]
picker_active = False

# Function to import videos
def get_videos(multiple):
    global picker_active
    # Return an empty set if the picker is already active
    if (picker_active):
        return []
    # Mark picker as active
    picker_active = True
    # Prompt for a file to be selected
    cli_logger.log(LogLevel.INFO, "Please select a file to analyse!")
    # Create variable to store videos
    videos = []
    # Check if multiple are allowed
    if multiple:
        # Inform the user multiple files are allowed
        cli_logger.log(LogLevel.INFO, "Multiple files can be selected!")
        # Select multiple files and return the result
        videos = filedialog.askopenfilenames(filetypes=valid_files)
    else:
        # Select one file and return the result
        videos = [filedialog.askopenfilename(filetypes=valid_files)]
    # Mark the picker as no longer active
    picker_active = False
    # Return the videos
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
    cap = None
    queue = None
    queue_size = 128
    stopped = False
    frames_interval = 0
    frames_done = 0
    frames_total = 0
    progress = 0

    def __init__(self, file, queue_size=128):
        self.file = file
        self.stopped = False
        self.queue = Queue(maxsize=queue_size)
        self.queue_size = queue_size
        self.cap = cv2.VideoCapture(self.file)
        self.frames_total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frames_interval = (1000 / self.cap.get(cv2.CAP_PROP_FPS)) / 1000

    def start(self):
        thread = Thread(target=self.update, args=())
        thread.setDaemon(True)
        thread.start()
        return self
    
    def stop(self):
        # Flag as stopped
        self.stopped = True
    
    def update(self):
        # Loop on thread
        while True:
            # Await a small sleep to try desync threads
            time.sleep(0.0001)
            # Return if reading has been stopped
            if (self.stopped):
                return
            # Check the queue has space left
            if (self.queue.qsize() < self.queue_size):
                # Read a frame from the stream
                (ret, frame) = self.cap.read()
                # Stop if a frame was not returned
                if (not ret):
                    self.stop()
                    return
                # Increment number of frames done
                self.frames_done += 1
                # Add the frame to the queue
                self.queue.put(frame)

    def read(self):
        # Return next frame in queue
        return self.queue.get()
    
    def can_read(self):
        # Return if there is items left in the queue
        return self.queue.qsize() > 0
    
    def get_progress(self):
        one_dp = "{:.1f}"
        no_dp = "{:.0f}"
        self.progress = (self.frames_done / self.frames_total) * 100
        return "Frame " + no_dp.format(self.frames_done) + "/" + no_dp.format(self.frames_total) + "(" + one_dp.format(self.progress) + "%)"
