import cv2
import functools
import numpy
import segmentation
from collections import deque
from itertools import chain

"""Functions for Connected-Component Labelling (More info: https://en.wikipedia.org/wiki/Connected-component_labeling)"""


"""Control function that stores objects and handles searching for new objects"""
def ccl(inp_frame):
    #Dictionary containing all objects found in a thresholded image
    objects = {}
    #Initialise object label
    object_label = 1

    #List to contain coordinates of all explored objects
    labelled = []
    pixel_search_offset = 0

    #Continually look for and explore new objects in the frame
    while True:
        #Find an unexplored pixel (this indicates a new object in the frame)
        search_pixel = find_new_object(inp_frame, labelled, pixel_search_offset)
        
        #Break while loop if no new pixel is found
        if search_pixel[0] == None: 
            break   
        pixel_search_offset = search_pixel[1]

        #Explore all pixels connected to search_pixel to find new object
        new_object = explore_object(inp_frame, search_pixel[0])
        #Add new_object to objects dictionary
        objects[object_label] = new_object
        #Update labelled array
        labelled = list(chain.from_iterable(objects.values()))

        #Increment object_label for next object
        object_label += 1

    #Return objects dictionary containing all objects found in a frame
    return objects

"""Function to iterate over image until an un-labelled foreground pixel is found"""
def find_new_objectOld(inp_frame, labelled):
    x_range = range(inp_frame.shape[0])
    y_range = range(inp_frame.shape[1])

    #Iterate over the image until a foreground pixel is found
    for x, _ in enumerate(x_range):
        for y, __ in enumerate(y_range):
            #Check if pixel is white (255) and not already labelled
            if inp_frame[x, y] == 255 and (x, y) not in labelled:
                return (x, y)

    #If no new pixels are found, return None
    return None

def find_new_object(inp_frame, labelled, start_offset):
    #Flatten inp_frame in to 1D array
    pixels = inp_frame.flatten()[start_offset:]
    #Get width of inp_frame in pixels
    row_width = inp_frame.shape[1]

    #Iterate through pixels, check if a pixel is foreground. If it is, calculate coordinate pair and make sure it is not in labelled, then return pair
    for i, value in enumerate(pixels):
        if value == 255:
            x_index = (i + start_offset) // row_width
            y_index = (i + start_offset) % row_width

            if (x_index, y_index) not in labelled:
                return (x_index, y_index), (i + start_offset)

    #If no new pixels are found, return None
    return None, 0

"""Function that carries out a breadth first search starting from start_pixel and keeping track of all pixels that are currently unlabelled.
   Returns a list of coordinates of all currently unexplored pixels in an object."""
def explore_object(inp_frame, start_pixel):
    #List containing coordinate pairs for all pixels in object
    new_object_coords = []
    #Queue to hold pixels waiting to be searched
    queue = deque()
    #Enqueue start_pixel to queue
    queue.append(start_pixel)
    while len(queue) > 0:
        #Deque pixel
        pixel = queue.popleft()
        if pixel not in new_object_coords:
            #Add pixel to new_object_coords
            new_object_coords.append(pixel)

            #Check if pixel above is foreground
            if inp_frame[pixel[0] - 1, pixel[1]] == 255 and pixel[0] > 0:
                queue.append((pixel[0] - 1, pixel[1]))

            #Check if pixel right is foreground
            if inp_frame[pixel[0], pixel[1] + 1] == 255 and pixel[1] < inp_frame.shape[1] - 1: 
                queue.append((pixel[0], pixel[1] + 1))

            #Check if pixel below is foreground
            if inp_frame[pixel[0] + 1, pixel[1]] == 255 and pixel[0] < inp_frame.shape[0] - 1:
                queue.append((pixel[0] + 1, pixel[1]))

            #Check if pixel left is foreground
            if inp_frame[pixel[0], pixel[1] - 1] == 255 and pixel[1] > 0:
                queue.append((pixel[0], pixel[1] - 1))

    return new_object_coords