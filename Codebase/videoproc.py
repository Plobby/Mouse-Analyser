import cv2
import threading

import segmentation as seg
import ccl
import time
import datetime

import multiprocessing as mp
from multiprocessing import Process, Queue
from threading import Thread
from itertools import chain, zip_longest

"""Function that processes a video stored at video_source to find mouse in all frames of video. If the mouse cannot be found in a given frame, it is saved for later.
   The next time the mouse is found, that bounding box is also applied to all prior frames in which it was not found.
   After processing all frames, the bounding box is drawn on all frames and the video is returned."""
def process_video_single(video_source, do_save_vid, output_location, func):
    #Dictionary containing bounding box locations for each frame (key = frame position)
    frame_bounding_boxes = {}
    #List of unprocessed frames, by frame position in video
    unprocessed = []
    #Threshold value to be applied to all frames, as calculated from the first frame
    video_threshold = 0
    
    #Open the video stored at video_source
    video = cv2.VideoCapture(video_source)

    # Get total frames of video
    frame_total = video.get(cv2.CAP_PROP_FRAME_COUNT)

    #Get first frame of video
    ret, frame = video.read()
    #Calculate threshold if a frame is returned (ret == true)
    if ret:
        video_threshold = seg.otsu_threshold(frame)
    counter = 0

    #Step through frames of video
    while video.isOpened():
        # Get frame number for current frame
        frame_pos = video.get(cv2.CAP_PROP_POS_FRAMES)
        # Calculate percentage of processing done
        percentage = (frame_pos / frame_total) * 100
        func(percentage)
        #Set default bounding box in case no bounding box is ever found
        frame_bounding_boxes[frame_pos] = [0, 0, 0, 0]
        #Calculate bounding box size for mouse in frame
        bounding_box = process_frame(frame, video_threshold)

        #If a bounding box is not found, save frame for later
        if bounding_box == None:
            unprocessed.append(frame_pos)
        #Else use the bounding box of the current frame as the bounding box for any unprocessed frames before it
        else:
            while len(unprocessed) > 0:
                frame_bounding_boxes[unprocessed.pop(0)] = bounding_box
            #Add current frame's bounding box to frame_bounding_boxes
            frame_bounding_boxes[frame_pos] = bounding_box

        print("Processed frame: " + str(counter))
        counter += 1
        #Get next frame of video and a flag indicating if there is a frame available
        ret, frame = video.read()

        #Break while loop if return flag is false
        if not ret:
            break
    
    #Initialise variables and VideoWriter object needed to save videos if do_save_vid flag is true
    if do_save_vid:
        #Split video_source string to find parent folder (source) and file name
        if '/' in video_source:
            split = video_source.split('/')
        elif '\\' in video_source:
            split = video_source.split('\\')
        
        file_name = split[-1].split('.')[0]    

        if output_location == "No Valid File Path Detected":
            output_location = "C:/mousehub_output"

        #Create cv2 VideoWriter object to output bounded video
        out = cv2.VideoWriter(output_location + "/" + file_name + '-bounded.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(video.get(cv2.CAP_PROP_FPS)), (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        print(output_location + "/" + file_name + '-bounded.mp4')

    #List containing data about the mouse from each frame (format: [mouseCentreOfMass, mouse_width, mouse_height])
    mouse_data = []

    #Draw bounding box on to each frame of video and calculate com, width & height
    for key, box in frame_bounding_boxes.items(): #Box contains [MinimumX, MaximumX, MinimumY, MaximumY] values for bounding box
        #Set frame position
        video.set(cv2.CAP_PROP_POS_FRAMES, key)
        #Get frame
        ret, frame = video.read()

        #Draw bounding box using box values
        if ret:
            #Draw sides
            for x in range(box[0], box[1] + 1):
                frame[x, box[2]] = [255, 0, 0]
                frame[x, box[3]] = [255, 0, 0]

            #Draw top and bottom
            for y in range(box[2], box[3] + 1):
                frame[box[0], y] = [255, 0, 0]
                frame[box[1], y] = [255, 0, 0]

        else:
            break
        
        #Find width of mouse
        mouse_width = box[3] - box[2]
        #Find height of mouseccl
        mouse_height = box[1] - box[0]
        #Find centre of mass of mouse
        mouse_com = (box[2] + (mouse_width / 2), box[0] + (mouse_height / 2))

        #Add mouse data to mouse_data (conventional coordinates i.e. (0,0) = bottom left corner)
        mouse_data.append([mouse_com, mouse_width, mouse_height])

        if do_save_vid:
            #Save bounded frame
            out.write(frame)

    #Release video
    video.release()
    
    #Release VideoWriter object if do_save_vid is true
    if do_save_vid:
        out.release()

    return mouse_data

def process_video(video_source, save, output_location, func):
    # Process count variable
    process_percent = 0.5
    process_count = int(mp.cpu_count() * process_percent)
    # Create new list for queue buffers
    process_queues = []
    for i in range(0, process_count):
        process_queues.append(Queue(maxsize=16))
    # Create a new multi queue input for the video
    reader = MultiQueueInput(video_source, process_queues)
    reader.start()
    start = time.time()
    print(str(reader.frames_total) + " input frames found")
    # Create new list for outputs
    outputs = {}
    # Create new list for processors
    processors = []
    for i in range(0, process_count):
        # Initialize output list
        outputs[i] = Queue()
        # Create and start processes
        proc = Process(target=processor_call, args=[reader.stopped, process_queues[i], outputs[i]])
        proc.start()
        processors.append(proc)
    # Join all processors back to main thread
    for proc in processors:
        proc.join()
    # Close reader to release resources
    reader.close()

    # Merge lists into one "joined" object
    output_lists = []
    for i in range(0, process_count):
        output_lists.append([])
        while (outputs[i].qsize() != 0):
            output_lists[i].append(outputs[i].get())
    my_sent = object()
    joined = [ele for ele in chain.from_iterable(zip_longest(*output_lists,fillvalue=my_sent)) if ele is not my_sent]

    # Iterate backwards over array and translate any missing boxes
    i = len(joined) - 1
    while (i >= 1):
        # Perform frame fix
        if (joined[i - 1] is None):
            if (joined[i] is None):
                joined[i - 1] = [0, 0, 0, 0]
            else:
                joined[i - 1] = joined[i]
        # Decrement counter
        i -= 1
    print(str(len(joined)) + " output frames generated")
    print("Processing time: " + str(datetime.timedelta(seconds=int(time.time() - start))))

    # Open the video stored at video_source
    video = cv2.VideoCapture(video_source)

    # Initialise variables and VideoWriter object needed to save videos if do_save_vid flag is true
    if save:
        # Split video_source string to find parent folder (source) and file name
        if '/' in video_source:
            split = video_source.split('/')
        elif '\\' in video_source:
            split = video_source.split('\\')
        
        file_name = split[-1].split('.')[0]    

        if output_location == "No Valid File Path Detected":
            output_location = "C:/mousehub_output"

        # Create cv2 VideoWriter object to output bounded video
        out = cv2.VideoWriter(output_location + "/" + file_name + '-bounded.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(video.get(cv2.CAP_PROP_FPS)), (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        print(output_location + "/" + file_name + '-bounded.mp4')

    # List containing data about the mouse from each frame (format: [mouseCentreOfMass, mouse_width, mouse_height])
    mouse_data = []

    # Draw bounding box on to each frame of video and calculate com, width & height
    for key, box in enumerate(joined, start=0): # Box contains [MinimumX, MaximumX, MinimumY, MaximumY] values for bounding box
        # Set frame position
        video.set(cv2.CAP_PROP_POS_FRAMES, key)
        #Get frame
        ret, frame = video.read()

        # Draw bounding box using box values
        if ret:
            # Draw sides
            for x in range(box[0], box[1] + 1):
                frame[x, box[2]] = [255, 0, 0]
                frame[x, box[3]] = [255, 0, 0]

            # Draw top and bottom
            for y in range(box[2], box[3] + 1):
                frame[box[0], y] = [255, 0, 0]
                frame[box[1], y] = [255, 0, 0]
        else:
            break
        
        # Find width of mouse
        mouse_width = box[3] - box[2]
        # Find height of mouseccl
        mouse_height = box[1] - box[0]
        # Find centre of mass of mouse
        mouse_com = (box[2] + (mouse_width / 2), box[0] + (mouse_height / 2))

        #Add mouse data to mouse_data (conventional coordinates i.e. (0,0) = bottom left corner)
        mouse_data.append([mouse_com, mouse_width, mouse_height])

        if save:
            # Save bounded frame
            out.write(frame)

    # Release video
    video.release()
    
    # Release VideoWriter object if do_save_vid is true
    if save:
        out.release()

    # Return the compiled mouse data
    return mouse_data

def processor_call(stopped, read_queue, outputs):
    # Variable to track frame index
    frame_index = 0
    # Iterate while reader running or queue has values
    while (stopped[0] or not read_queue.empty()):
        # Attempt to read the next frame
        try:
            # Read frame
            frame = read_queue.get(block=False)
            # Calculate threshold
            video_threshold = seg.otsu_threshold(frame)
            # Calculate bounding box size for mouse in frame
            bounding_box = process_frame(frame, video_threshold)
            # Add current frame's bounding box to outputs
            outputs.put(bounding_box)
            # Increment frame index
            frame_index += 1
        except Exception as ex:
            print("Error reading frame: " + str(ex))

"""Function that attempt to find the mouse in a frame. If no mouse cannot be clearly found, return None. Else, return bounding box min and max values"""
def process_frame(frame, threshold):
     #Create segmented version of frame
    segmented = seg.threshold_segment(frame, threshold)
    #Find all objects in segmented frame using ccl
    objects = ccl.ccl(segmented)
    
    #Create array to hold sorted objects keys
    sorted_keys = sorted(objects, key=lambda k: len(objects[k]), reverse=True)
    
    #Set target_object to the 2nd largest object in frame (assuming feed station is largest, mouse 2nd largest)
    target_object = sorted_keys[1]
    
    #Find extreme pixels in target object
    min_x = frame.shape[0]
    max_x = 0
    min_y = frame.shape[1]
    max_y = 0

    for coord in objects[target_object]:
        if coord[0] < min_x:
            min_x = coord[0]
        if coord[0] > max_x:
            max_x = coord[0]
        if coord[1] < min_y:
            min_y = coord[1]
        if coord[1] > max_y:
            max_y = coord[1]

    #Apply heuristics to find invalid bounding boxes and return None
    
    #Height/width is too great
    if ((max_x - min_x) / (max_y - min_y) > 4):
        return None
    #Width/height is too great
    if ((max_y - min_y) / (max_x - max_y) > 4):
        return None
    #Absolute height is too great
    if (max_x - min_x > frame.shape[0] / 4):
        return None
    #Absolute width is too great
    if (max_y - min_y > frame.shape[1] / 4):
        return None

    #Return bounding box information
    return min_x, max_x, min_y, max_y

class MultiQueueInput():
    # Member variables
    cap = None
    file = None
    process_queues = None
    queue_count = 0
    queue_next = 0
    queue_size = 16
    stopped = [False]
    frames_fps = 0
    frames_width = 0
    frames_height = 0
    frames_interval = 0
    frames_done = 0
    frames_total = 0
    progress = 0

    def __init__(self, file, process_queues):
        # Bind variables
        self.file = file
        self.process_queues = process_queues
        self.queue_count = len(process_queues)
        # Open video capture
        self.cap = cv2.VideoCapture(self.file)
        # Get video properties
        self.frames_total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frames_fps = int(round(self.cap.get(cv2.CAP_PROP_FPS)))
        self.frames_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frames_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frames_interval = (1000 / self.frames_fps) / 1000
        # Close video capture
        self.cap.release()
        self.cap = None

    def start(self):
        # Flag as not stopped
        self.stopped[0] = False
        # Create new capture object
        self.cap = cv2.VideoCapture(self.file)
        # Start reading frames
        thread = Thread(target=self.update, daemon=True)
        thread.start()
        return self
    
    def stop(self):
        # Flag as stopped
        self.stopped[0] = True
    
    def close(self):
        # Flag as stopped
        self.stopped[0] = True
        self.cap.release()
    
    def update(self):
        # Loop on thread
        while (not self.stopped[0]):
            # Get the next target
            target = self.process_queues[self.queue_next]
            # Check the queue has space left
            if (target.qsize() < self.queue_size):
                # Increment queue tracker
                self.queue_next += 1
                if (self.queue_next >= self.queue_count):
                    self.queue_next = 0
                # Read a frame from the stream
                (ret, frame) = self.cap.read()
                # Stop if a frame was not returned
                if (not ret):
                    self.stop()
                    return
                # Increment number of frames done
                self.frames_done += 1
                # Add the frame to the queue
                target.put(frame, block=True)
                # Wait small delay
                time.sleep(0.0002)
        # Release capture object
        self.cap.release()
        self.cap = None
    
    def get_progress(self):
        one_dp = "{:.1f}"
        no_dp = "{:.0f}"
        self.progress = (self.frames_done / self.frames_total) * 100
        return "Frame " + no_dp.format(self.frames_done) + "/" + no_dp.format(self.frames_total) + "(" + one_dp.format(self.progress) + "%)"