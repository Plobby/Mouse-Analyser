import cv2
import functools
import numpy
import segmentation
from collections import deque
from itertools import chain

"""Functions for Connected-Component Labelling (More info: https://en.wikipedia.org/wiki/Connected-component_labeling)"""


"""Control function that stores objects and handles searching for new objects"""
def CCL(inpFrame):
    #Dictionary containing all objects found in a thresholded image
    objects = {}
    #Initialise object label
    objectLabel = 1

    #List to contain coordinates of all explored objects
    labelled = []
    #List to contain valid searchPixels (initialised with top left-most pixel)
    searchPixels = [(0, 0)]
    minSearchX = 0

    #Continually look for and explore new objects in the frame
    while True:
        #Find an unexplored pixel (this indicates a new object in the frame)
        searchPixel = findNewObject(inpFrame, labelled, minSearchX)

        #Break while loop if no new pixel is found
        if searchPixel == None: 
            break

        #Add searchPixel to searchPixels
        searchPixels.append(searchPixel)

        #Set minSearchX to highest X value in for searchPixels
        minSearchX = max(searchPixels, key=lambda coord: coord[0])

        #Explore all pixels connected to searchPixel to find new object
        newObject = exploreObject(inpFrame, searchPixel)
        #Add newObject to objects dictionary
        objects[objectLabel] = newObject
        #Update labelled array
        labelled = list(chain.from_iterable(objects.values()))

        #Increment objectLabel for next object
        objectLabel += 1

    #Return objects dictionary containing all objects found in a frame
    return objects

"""Function to iterate over image until an un-labelled foreground pixel is found"""
def findNewObject(inpFrame, labelled, xMin):
    xRange = range(xMin, inpFrame.shape[0])
    yRange = range(inpFrame.shape[1])

    #Iterate over the image until a foreground pixel is found
    for x, _ in enumerate(xRange):
        for y, __ in enumerate(yRange):
            #Check if pixel is white (255) and not already labelled
            if inpFrame[x, y] == 255 and (x, y) not in labelled:
                return (x, y)

    #If no new pixels are found, return None
    return None

"""Function that carries out a breadth first search starting from startPixel and keeping track of all pixels that are currently unlabelled.
   Returns a list of coordinates of all currently unexplored pixels in an object."""
def exploreObject(inpFrame, startPixel):
    #Queue to hold the next pixels to be searched
    searchQueue = deque()
    #Enqueue the startPixel coordinates
    searchQueue.append(startPixel)
    #List containing coordinates of new object's pixels
    newObjectCoords = []

    #Continually explore neighbouring pixels until no new unexplored pixels are found
    while len(searchQueue) > 0:
        #Pop pixel to be explored from searchQueue
        pixel = searchQueue.popleft()

        if pixel not in newObjectCoords:
            #Add pixel to newObjectCoords
            newObjectCoords.append(pixel)
            
            #Check if pixel above is foreground and has not already been explored for this object
            if ((pixel[0] > 0) and (inpFrame[pixel[0] - 1, pixel[1]] == 255) and ((pixel[0] - 1, pixel[1]) not in newObjectCoords)):
                #Add pixel above to searchQueue
                searchQueue.append((pixel[0] - 1, pixel[1]))
        
            #Check if pixel right is foreground and has not already been explored for this object
            if ((pixel[1] < len(inpFrame[1]) - 1) and (inpFrame[pixel[0], pixel[1] + 1] == 255) and ((pixel[0], pixel[1] + 1) not in newObjectCoords)):
                #Add pixel right to searchQueue
                searchQueue.append((pixel[0], pixel[1] + 1))
        
            #Check if pixel below is foreground and has not already been explored for this object
            if ((pixel[0] < len(inpFrame) - 1) and (inpFrame[pixel[0] + 1, pixel[1]] == 255) and ((pixel[0] + 1, pixel[1]) not in newObjectCoords)):
                #Add pixel below to searchQueue
                searchQueue.append((pixel[0] + 1, pixel[1]))

            #Check if pixel left is foreground and has not already been explored for this object
            if ((pixel[1] > 0) and (inpFrame[pixel[0], pixel[1] - 1] == 255) and ((pixel[0], pixel[1] - 1) not in newObjectCoords)):
                #Add pixel left to searchQueue
                searchQueue.append((pixel[0], pixel[1] - 1))

    return newObjectCoords
