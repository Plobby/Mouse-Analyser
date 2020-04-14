import cv2
import functools
import numpy
import numpy as np

""" Implementation of Otsu's thresholding algorithm to find best threshold for a grayscale frame
More info: http://www.labbookpages.co.uk/software/imgProc/otsuThreshold.html """

def otsuThreshold(inpFrame):
    #Turn frame to greyscale
    inpFrame = cv2.cvtColor(inpFrame, cv2.COLOR_BGR2GRAY)
    #Number of colour channels
    channels = 256
    #Find histogram representing inpFrame
    hist = cv2.calcHist([inpFrame.astype("float32")], [0], None, [channels], [0, 256])
    #Find total number of pixels in image
    totalPixels = sum(hist)
    
    #Keep track of best threshold value and its BC Variance
    bestThreshold = 0
    bestBCVariance = 0.0
    #Test each possible threshold and update bestThreshold
    for threshold in range(0, channels):
        #Find total number of pixels lower than threshold
        pixelsBackground = sum(hist[:threshold + 1])
        #Find total number of pixels greater than threshold
        pixelsForeground = sum(hist[threshold + 1:])

        #Calculate weight of background pixels
        weightBackground = pixelsBackground / totalPixels
        #Calculate mean of background pixels
        sumValues = 0
        for i in range(0, threshold):
            sumValues += hist[i] * i

        meanBackground = sumValues / pixelsBackground

        #Calculate weight of foreground pixels
        weightForeground = pixelsForeground / totalPixels
        #Calculate mean of foreground pixels
        sumValues = 0
        for i in range(threshold, 256):
            sumValues += hist[i] * i

        #print(pixelsForeground + " total foreground pixels!")
        meanForeground = sumValues / pixelsForeground

        #Calculate Between Class Variance for the frame
        betweenClassVariance = (weightBackground * weightForeground) * ((meanBackground - meanForeground) ** 2)

        #Update bestThreshold & bestBCVariance with highest BC Variance
        if betweenClassVariance > bestBCVariance:
            bestThreshold = threshold
            bestBCVariance = betweenClassVariance

    #Return bestThreshold
    return bestThreshold * 0.5

""" Function to segment fore and background of a frame using threshold value """
def thresholdSegment(inpFrame, threshold):
    #Turn frame to greyscale
    inpFrame = cv2.cvtColor(inpFrame, cv2.COLOR_BGR2GRAY)
    #Create a copy of inpFrame to be modified
    frame = numpy.zeros(inpFrame.shape, dtype=numpy.uint8)

    # #Percentages of x and y to not include in foreground
    borderPercentX = 0.05
    borderPercentY = 0.05

    xRange = range(int(inpFrame.shape[0] * borderPercentX), int(inpFrame.shape[0] - (inpFrame.shape[0] * borderPercentX)))
    yRange = range(int(inpFrame.shape[1] * borderPercentY), int(inpFrame.shape[1] - (inpFrame.shape[1] * borderPercentX)))
    
    #Iterate through inpFrame (a 2D array), changing pixel value to white or black based on threshold
    for x, _ in enumerate(xRange):
        for y, __ in enumerate(yRange):
            if inpFrame[x, y] < threshold:
                frame[x, y] = 255
            else:
                frame[x, y] = 0

    return frame

def deNoise(currentFrame, prevFrame):
    return None