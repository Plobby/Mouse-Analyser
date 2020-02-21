import cv2
import threading

import Segmentation as seg
import CCL

def processFrame(frame):
    #Find the threshold for the frame
    videoThreshold = seg.otsuThreshold(frame)
    
    #Create segmented version of frame
    segmented = seg.thresholdSegment(frame, videoThreshold)
    #Find all objects in segmented frame using CCL
    objects = CCL.CCL(segmented)
    
    #Create array to hold sorted objects keys
    sortedKeys = []
    
    #Sort keys of objects in reverse order by length of value associated with key
    for key in sorted(objects, key=lambda key: len(objects[key]), reverse=True):
        sortedKeys.append(key)
    
    #Set targetObject to the 2nd largest object in frame (feed station is largest, mouse 2nd largest)
    targetObject = sortedKeys[1]
    
    #Find extreme pixels in largest object
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

    #Draw bounding box around largest object in original frame
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            #Draw top and bottom of bounding box
            if ((x == MinX) or (x == MaxX)) and ((y >= MinY) and (y <= MaxY)):
                frame[x, y] = [255, 0, 0]
            #Draw sides of bounding box
            elif ((x >= MinX) and (x <= MaxX)) and ((y == MinY) or (y == MaxY)):
                frame[x, y] = [255, 0, 0]

    #Find center of mass of mouse by finding middle of bounding box
    xCOM = MinX + ((MaxX - MinX) / 2)
    yCOM = MinY + ((MaxY - MinY) / 2)

    #Return bounded frame and center of mass for x and y
    return frame, xCOM, yCOM