import cv2
import functools
import numpy
import Segmentation
from collections import deque

"""Functions for Connected-Component Labelling (More info: https://en.wikipedia.org/wiki/Connected-component_labeling)"""


"""Control function that stores objects and handles searching for new objects"""
def CCL(inpFrame):
    #Dictionary containing all objects found in a thresholded image
    objects = {}
    #Initialise object label
    objectLabel = 1

    #Continually look for and explore new objects in the frame
    while True:
        #Create list to contain coordinate tuples of all currently labelled pixels
        labelled = []
        #Populate list with coordinates of all pixels in all objects
        for key in objects.keys():
            for coord in objects[key]:
                labelled.append(coord)

        #Find an unexplored pixel (this indicates a new object in the frame)
        searchPixel = findNewObject(inpFrame, labelled)
        #Break while loop if no new pixel is found
        if searchPixel == None:
            break

        #Explore all pixels connected to searchPixel to find new object
        newObject = exploreObject(inpFrame, searchPixel, labelled)
        #Add newObject to objects dictionary
        objects[objectLabel] = []
        for newCoord in newObject:
            objects[objectLabel].append(newCoord)

        print(len(newObject))
        #Increment objectLabel for next object
        objectLabel += 1

    print(objects.keys())
    #Return objects dictionary containing all objects found in a frame
    return objects




"""Function to iterate over image until an un-labelled foreground pixel is found"""
def findNewObject(inpFrame, labelled):
    #Iterate over the image until a foreground pixel is found
    for x in range(inpFrame.shape[0]):
        for y in range(inpFrame.shape[1]):
            #Check if pixel is white (255)
            if inpFrame[x, y] == 255:
                #Check that the pixel is not already labelled
                if (x, y) not in labelled:
                    print("found new object " + str(x) + ", " + str(y))
                    #If the pixel is unlabelled, return a tuple containing the coordinates
                    return (x, y)

    #If no new pixels are found, return None
    return None

"""Function that carries out a breadth first search starting from startPixel and keeping track of all pixels that are currently unlabelled.
   Returns a list of tuples containing coordinates of all currently unexplored pixels in an object."""
def exploreObject(inpFrame, startPixel, labelled):
    print("Entered exploreObject()")
    #Queue to hold the next pixels to be searched
    searchQueue = deque()
    #Enqueue the startPixel coordinates
    searchQueue.append(startPixel)
    #List of tuples containing coordinates of new object's pixels
    newObjectCoords = []

    #Continually explore neighbouring pixels until no new (unlabelled) pixels are found
    while len(searchQueue) > 0:
        #Pop pixel to be explored from searchQueue
        pixel = searchQueue.popleft()
        #Add pixel to newObjectCoords
        newObjectCoords.append(pixel)

        """Error is in the following section, never entering the second condition for all four parts"""

        #Search above (if available)
        if pixel[0] > 0:
            #Check if pixel above is foreground and unlabelled and not already been explored for this object
            if (inpFrame[pixel[0] + 1, pixel[1]] == 255) and (pixel not in labelled) and (pixel not in newObjectCoords): # and (pixel not in labelled) and (pixel not in newObjectCoords)
                #Add pixel above to searchQueue
                searchQueue.append((pixel[0] + 1, pixel[1]))

        #Search right (if available)
        if pixel[1] < len(inpFrame[0] - 1):
            #Check if pixel right is foreground and unlabelled and not already been explored for this object
            if (inpFrame[pixel[0], [pixel[1] + 1] == 255) and (pixel not in labelled) and (pixel not in newObjectCoords): # and (pixel not in labelled) and (pixel not in newObjectCoords)
                #Add pixel right to searchQueue
                searchQueue.append((pixel[0], pixel[1] + 1))

        #Search below (if available)
        if pixel[0] < len(inpFrame - 1):
            #Check if pixel below is foreground and unlabelled and not already been explored for this object
            if (inpFrame[pixel[0] - 1, [pixel[1]] == 255) and (pixel not in labelled) and (pixel not in newObjectCoords): #and (pixel not in labelled) and (pixel not in newObjectCoords)
                #Add pixel below to searchQueue
                searchQueue.append((pixel[0] - 1, pixel[1]))

        #Search left (if available)
        if pixel[1] > 0:
            #Check if pixel left is foreground and unlabelled and not already been explored for this object
            if (inpFrame[pixel[0], pixel[1] - 1] == 255) and (pixel not in labelled) and (pixel not in newObjectCoords): #and (pixel not in labelled) and (pixel not in newObjectCoords)
                #Add pixel left to searchQueue
                searchQueue.append((pixel[0], pixel[1] - 1))

    return newObjectCoords
