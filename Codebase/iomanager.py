from tkinter import filedialog
import cv2
import logging
from logging import LogLevel

# Create variable with allowed file types
VALID_FILES = [("mpeg videos", "*.mpg"), ("mp4 videos", "*.mp4"), ("avi videos", "*.avi")]

# Function to import videos
def get_videos(multiple):
    # Prompt for a file to be selected
    logging.log(LogLevel.INFO, "Please select a file to analyse!")
    # Create variable to store videos
    videos = []
    # Check if multiple are allowed
    if multiple:
        # Inform the user multiple files are allowed
        logging.log(LogLevel.INFO, "Multiple files can be selected!")
        # Select multiple files and return the result
        videos = filedialog.askopenfilenames(filetypes=VALID_FILES)
    else:
        # Select one file and return the result
        videos = [filedialog.askopenfilename(filetypes=VALID_FILES)]
    # Open the videos and return
    return open_files(videos)

#Function to save a *LIST* of CV2 VideoCapture objects
def save_videos(videoCaps, outputLocation):
    if outputLocation == None: #This is for GUI mode, where a directory is not already given
        #Open folder selection dialog box
        outputLocation = filedialog.askdirectory()

    #Index for giving unique names to each video being saved
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
        #Save video
        save_videos([cap], outputLocation=None)
        # Release the capture variable
        cap.release()
        # Destroy all cv2 windows
        cv2.destroyAllWindows()
    return videos