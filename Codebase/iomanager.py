# Imports
from tkinter import filedialog
import cv2

# Create variable with allowed file types
VALID_FILES = [("mp4 videos", "*.mp4"), ("avi videos", "*.avi"), ("mpeg videos", "*.mpg")]

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
            # Show the greyscale frame
            cv2.imshow('Video ' + str(index), gray)
            # Wait for the next key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release the capture variable
        cap.release()
        # Destroy all cv2 windows
        cv2.destroyAllWindows()
    return videos