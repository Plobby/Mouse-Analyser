# Imports
from tkinter import filedialog
from tkinter import Tk
from PIL import ImageTk, Image
import PIL as PIL
import numpy
import cv2
import gui

# Hide the main tkinter window
ROOT = Tk()
ROOT.withdraw()

# Create variable with allowed file types
VALID_FILES = [ ("mpeg videos", "*.mpg"), ("avi videos", "*.avi"), ("mp4 videos", "*.mp4")]

# Function to import videos
def get_videos(multiple):
    # Prompt for a file to be selected
    print("Please select a file to analyse!")
    # Create variable to store videos
    videos = []
    # Check if multiple are allowed
    if multiple:
        # Inform the user multiple files are allowed
        print("Multiple files can be selected!")
        # Select multiple files and return the result
        videos = filedialog.askopenfilenames(filetypes=VALID_FILES)
    else:
        # Select one file and return the result
        videos = [filedialog.askopenfilename(filetypes=VALID_FILES)]
    # Open the videos and return
    return open_files(videos)

# Function to attempt to open files with openCV
def open_files(videos):
    # Variable counter to store the video index
    index = 0
    # Attempt to open the video files
    for video in videos:
        # Increment the video index
        index = index + 1
        # Capture video and store in a variable
        cap = cv2.VideoCapture(video)
        # Iterate while capture is opened
        while (cap.isOpened()):
            # Read the next return and get the frame
            ret, frame = cap.read()
            # Break if no frame was returned
            if (not ret):
                break
            # Convert the frame to greyscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #Covert to PIL
            #photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(gray))
            #Attempts to show on canvas
            #VideoFrame['image'] = photo
            # Show the greyscale frame
            cv2.imshow(gui.VideoPage.VideoFrame, gray)
            # Wait for the next key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release the capture variable
        cap.release()
        # Destroy all cv2 windows
        cv2.destroyAllWindows()
    return videos
