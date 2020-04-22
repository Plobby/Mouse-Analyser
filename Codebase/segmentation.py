import cv2
import functools
import numpy
import numpy as np

""" Implementation of Otsu's thresholding algorithm to find best threshold for a grayscale frame
More info: http://www.labbookpages.co.uk/software/imgProc/otsu_threshold.html """

def otsu_threshold(inp_frame):
    #Turn frame to greyscale
    inp_frame = cv2.cvtColor(inp_frame, cv2.COLOR_BGR2GRAY)
    #Number of colour channels
    channels = 256
    #Find histogram representing inp_frame
    hist = cv2.calcHist([inp_frame.astype("float32")], [0], None, [channels], [0, 256])
    #Find total number of pixels in image
    total_pixels = sum(hist)
    
    #Keep track of best threshold value and its BC Variance
    best_threshold = 0
    best_bc_variance = 0.0
    #Test each possible threshold and update best_threshold
    for threshold in range(0, channels):
        #Find total number of pixels lower than threshold
        pixels_background = sum(hist[:threshold + 1])
        #Find total number of pixels greater than threshold
        pixels_foreground = sum(hist[threshold + 1:])

        #Calculate weight of background pixels
        weight_background = pixels_background / total_pixels
        #Calculate mean of background pixels
        sum_values = 0
        for i in range(0, threshold):
            sum_values += hist[i] * i

        mean_background = 0
        if (not pixels_background == 0):
            mean_background = sum_values / pixels_background

        #Calculate weight of foreground pixels
        weight_foreground = pixels_foreground / total_pixels
        #Calculate mean of foreground pixels
        sum_values = 0
        for i in range(threshold, 256):
            sum_values += hist[i] * i

        #print(pixels_foreground + " total foreground pixels!")
        mean_foreground = 0
        if (not pixels_foreground == 0):
            mean_foreground = sum_values / pixels_foreground

        #Calculate Between Class Variance for the frame
        between_class_variance = (weight_background * weight_foreground) * ((mean_background - mean_foreground) ** 2)

        #Update best_threshold & best_bc_variance with highest BC Variance
        if between_class_variance > best_bc_variance:
            best_threshold = threshold
            best_bc_variance = between_class_variance

    #Return best_threshold
    return best_threshold * 0.5

""" Function to segment fore and background of a frame using threshold value """
def threshold_segment(inp_frame, threshold):
    #Turn frame to greyscale
    inp_frame = cv2.cvtColor(inp_frame, cv2.COLOR_BGR2GRAY)
    #Create a copy of inp_frame to be modified
    frame = numpy.zeros(inp_frame.shape, dtype=numpy.uint8)

    # #Percentages of x and y to not include in foreground
    border_percent_x = 0.05
    border_percent_y = 0.05

    x_range = range(int(inp_frame.shape[0] * border_percent_x), int(inp_frame.shape[0] - (inp_frame.shape[0] * border_percent_x)))
    y_range = range(int(inp_frame.shape[1] * border_percent_y), int(inp_frame.shape[1] - (inp_frame.shape[1] * border_percent_x)))
    
    #Iterate through inp_frame (a 2D array), changing pixel value to white or black based on threshold
    for _, x in enumerate(x_range):
        for __, y in enumerate(y_range):
            if inp_frame[x, y] < threshold:
                frame[x, y] = 255
            else:
                frame[x, y] = 0

    return frame

def de_noise(current_frame, prev_frame):
    return None