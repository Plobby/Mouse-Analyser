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
    
    #Find largest object in frame
    largestObjectKey = 1;
    for key in objects.keys():
        if len(objects[key]) > len(objects[largestObjectKey]):
            largestObjectKey = key

    #Remove all but the largest object from the foreground
    for x in range(segmented.shape[0]):
        for y in range(segmented.shape[1]):
            if (x, y) not in objects[largestObjectKey]:
                segmented[x, y] = 0
    
    #Find extreme pixels in largest object
    MinX = frame.shape[0]
    MaxX = 0
    MinY = frame.shape[1]
    MaxY = 0

    for coord in objects[largestObjectKey]:
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

    return frame