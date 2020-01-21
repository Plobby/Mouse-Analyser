import cv2
import functools
import PIL

#Implementation of Otsu's thresholding algorithm to find best threshold for a given frame
def otsuThreshold(inpFrame):
    #Number of colour channels
    channels = 256
    #Find histogram representing inpFrame
    hist = cv2.calcHist([inpFrame.astype("float32")], [0], None, [channels], [0, 256])
    #Find total number of pixels in image
    totalPixels = functools.reduce(lambda a, b: a + b, hist)

    print(hist[:10])
    
    bestThreshold = 0
    bestBCVariance = 0.0
    for threshold in range(0, channels):
        #Find total number of pixels lower than threshold
        pixelsBackground = functools.reduce(lambda a, b: (a + b), hist[:threshold + 1])
        #Find total number of pixels greater than threshold
        pixelsForeground = functools.reduce(lambda a, b: (a + b), hist[threshold:])

        #Calculate weight of background pixels
        weightBackground = pixelsBackground / totalPixels
        #Calculate mean of background pixels
        sumValues = 0
        for i in range(0, threshold):
            sumValues = hist[i] * i

        meanBackground = sumValues / pixelsBackground

        #Calculate weight of foreground pixels
        weightForeground = pixelsForeground / totalPixels
        #Calculate mean of foreground pixels
        sumValues = 0
        for i in range(threshold, 256):
            sumValues = hist[i] * i

        meanForeground = sumValues / pixelsForeground

        #Calculate Between Class Variance for the frame
        betweenClassVariance = (weightBackground * weightForeground) * ((meanBackground - meanForeground) ** 2)

        #Update bestThreshold & bestBCVariance with highest BC Variance
        if betweenClassVariance > bestBCVariance:
            bestThreshold = threshold
            bestBCVariance = betweenClassVariance

    return bestThreshold
