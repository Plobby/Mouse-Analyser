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
    pixelSearchOffset = 0

    #Continually look for and explore new objects in the frame
    while True:
        #Find an unexplored pixel (this indicates a new object in the frame)
        searchPixel = findNewObject(inpFrame, labelled, pixelSearchOffset)
        
        #Break while loop if no new pixel is found
        if searchPixel[0] == None: 
            break   
        pixelSearchOffset = searchPixel[1]

        #Explore all pixels connected to searchPixel to find new object
        newObject = exploreObject(inpFrame, searchPixel[0])
        #Add newObject to objects dictionary
        objects[objectLabel] = newObject
        #Update labelled array
        labelled = list(chain.from_iterable(objects.values()))

        #Increment objectLabel for next object
        objectLabel += 1

    #Return objects dictionary containing all objects found in a frame
    return objects

"""Function to iterate over image until an un-labelled foreground pixel is found"""
def findNewObjectOld(inpFrame, labelled):
    xRange = range(inpFrame.shape[0])
    yRange = range(inpFrame.shape[1])

    #Iterate over the image until a foreground pixel is found
    for x, _ in enumerate(xRange):
        for y, __ in enumerate(yRange):
            #Check if pixel is white (255) and not already labelled
            if inpFrame[x, y] == 255 and (x, y) not in labelled:
                return (x, y)

    #If no new pixels are found, return None
    return None

def findNewObject(inpFrame, labelled, startOffset):
    #Flatten inpFrame in to 1D array
    pixels = inpFrame.flatten()[startOffset:]
    #Get width of inpFrame in pixels
    rowWidth = inpFrame.shape[1]

    #Iterate through pixels, check if a pixel is foreground. If it is, calculate coordinate pair and make sure it is not in labelled, then return pair
    for i, value in enumerate(pixels):
        if value == 255:
            xIndex = (i + startOffset) // rowWidth
            yIndex = (i + startOffset) % rowWidth

            if (xIndex, yIndex) not in labelled:
                return (xIndex, yIndex), (i + startOffset)

    #If no new pixels are found, return None
    return None, 0

"""Function that carries out a breadth first search starting from startPixel and keeping track of all pixels that are currently unlabelled.
   Returns a list of coordinates of all currently unexplored pixels in an object."""
def exploreObject(inpFrame, startPixel):
    #List containing coordinate pairs for all pixels in object
    newObjectCoords = []
    #Queue to hold pixels waiting to be searched
    queue = deque()
    #Enqueue startPixel to queue
    queue.append(startPixel)
    while len(queue) > 0:
        #Deque pixel
        pixel = queue.popleft()
        if pixel not in newObjectCoords:
            #Add pixel to newObjectCoords
            newObjectCoords.append(pixel)

            #Check if pixel above is foreground
            if inpFrame[pixel[0] - 1, pixel[1]] == 255 and pixel[0] > 0:
                queue.append((pixel[0] - 1, pixel[1]))

            #Check if pixel right is foreground
            if inpFrame[pixel[0], pixel[1] + 1] == 255 and pixel[1] < inpFrame.shape[1] - 1: 
                queue.append((pixel[0], pixel[1] + 1))

            #Check if pixel below is foreground
            if inpFrame[pixel[0] + 1, pixel[1]] == 255 and pixel[0] < inpFrame.shape[0] - 1:
                queue.append((pixel[0] + 1, pixel[1]))

            #Check if pixel left is foreground
            if inpFrame[pixel[0], pixel[1] - 1] == 255 and pixel[1] > 0:
                queue.append((pixel[0], pixel[1] - 1))

    return newObjectCoords