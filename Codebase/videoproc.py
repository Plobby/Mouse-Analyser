import cv2
import threading

import Segmentation as seg
import CCL

"""Function that processes a video to find mouse in all frames of video. If the mouse cannot be found in a given frame, it is saved for later.
   The next time the mouse is found, that bounding box is also used for all prior frames in which it was not found.
   After processing all frames, the bounding box is drawn on all frames and the video is returned."""
def processVideo(video):
    #Dictionary containing bounding box locations for each frame
    frameBoundingBoxes = {}
    #List of unprocessed frames, by frame position in video
    unprocessed = []
    #Threshold value to be applied to all frames, as calculated from the first frame
    videoThreshold = 0

    #Get first frame of video
    ret, frame = video.read()
    #Calculate threshold if a frame is returned (ret == true)
    if ret:
        videoThreshold = seg.otsuThreshold(frame)

    #Step through frames of video
    while True:
        #Get frame number for current frame
        framePos = video.get(cv2.CAP_PROP_POS_FRAMES)
        #Calculate bounding box size for mouse in frame
        boundingBox = processFrame(frame, videoThreshold)

        #If the size difference between the two largest objects in the frame is too different, save frame for later
        if boundingBox == None:
            unprocessed.append(framePos)
        #Else use the bounding box of the current frame as the bounding box for unprocessed frames before it
        else:
            while len(unprocessed) > 0:
                frameBoundingBoxes[unprocessed.pop(0)] = boundingBox   
            #Add current frame's bounding box to frameBoundingBoxes
            frameBoundingBoxes[framePos] = boundingBox

        #Get next frame of video and a flag indicating if there is a frame available
        ret, frame = video.read()
        #Break while loop if return flag is false
        if not ret:
            break
        
    #Draw bounding box on to each frame of video
    for key, box in frameBoundingBoxes.items(): #Box contains [MinimumX, MaximumX, MinimumY, MaximumY] values for bounding box
        #Set frame position
        video.set(cv2.CAP_PROP_POS_FRAMES, key)
        #Get frame
        ret, frame = video.read()

        #Draw bounding box using box values
        for x in range(frame.shape[0]):
            for y in range(frame.shape[1]):
                #Draw top and bottom of bounding box
                if ((x == box[0]) or (x == box[1])) and ((y >= box[2]) and (y <= box[3])):
                    frame[x, y] = [255, 0, 0]
                #Draw sides of bounding box
                elif ((x >= box[0]) and (x <= box[1])) and ((y == box[2]) or (y == box[3])):
                    frame[x, y] = [255, 0, 0]
    
    #Return video with bounding boxes drawn
    return video

"""Function that attempt to find the mouse in a frame. If no mouse can be clearly found, return None. Else, return bounding box min and max values"""
def processFrame(frame, threshold):
     #Create segmented version of frame
    segmented = seg.thresholdSegment(frame, threshold)
    #Find all objects in segmented frame using CCL
    objects = CCL.CCL(segmented)
    
    #Create array to hold sorted objects keys
    sortedKeys = []
    
    #Sort keys of objects in reverse order by length of value associated with key
    for key in sorted(objects, key=lambda key: len(objects[key]), reverse=True):
        sortedKeys.append(key) 
    
    #Check that first and second largest objects are of similar sizes
    if (objects[sortedKeys[1]] / objects[sortedKeys[0]]) > 0.8:
        #Set targetObject to the 2nd largest object in frame (feed station is largest, mouse 2nd largest)
        targetObject = sortedKeys[1]
    else:
        return None
    
    #Find extreme pixels in target object
    MinX = frame.shape[0]
    MaxX = 0
    MinY = frame.shape[1]
    MaxY = 0

    for coord in objects[targetObject]:
        if coord[0] < MinX:
            MinX = coord[0]
        if coord[0] > MaxX:
            MaxX = coord[0]
        if coord[1] < MinY:
            MinY = coord[1]
        if coord[1] > MaxY:
            MaxY = coord[1]

    return MinX, MaxX, MinY, MaxY