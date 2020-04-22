import tkinter as tk
from math import *
# MatPlotLib imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # Importing figure canvas for tkinter integration and also the navigation toolbar
from matplotlib.backend_bases import key_press_handler # Keypress handler
from matplotlib.figure import Figure # Figure is used for tkinter integration
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

class DataGraph():
    # Constructor
    def __init__(self):
        self._x_list = []
        self._y_list = []

    # Function to create a stacked bar chart
    def create_stacked_bar_chart(self, f, time_per_pos, time_per_bar, pos_meaning, pos_list):
        inner_plot = f.add_subplot(1,1,1)
        index_dict = []
        if time_per_bar > time_per_pos: # The time period per bar *must* be larger than the gap that the positions are reported in - else the program will break.
            # First job is to seperate pos_list into meanings.
            temp_list = []

            for meaning in pos_meaning: # For each meaning in the dict of meanings....
                item_checker = pos_meaning[meaning] # Set the checker to the current meaning.
                for x in range(0, len(pos_list)-1): # For each item in the position list
                    if pos_list[x] == item_checker: # Check if the current value is the one being searched for
                        temp_list.append(1) # If it is, append 1 to the temporary list
                    else: # If it isn't...
                        temp_list.append(0) # ... append 0.


                index_dict += [temp_list] # Slowly creating a 2d list by storing each kind of action as a binary list of whether it's currently being performed.
                temp_list = [] # Empty the temporary list once it's finished :)
            indexDict = []
            temp_list = []

            # Next step is to turn the new binary lists into graphable values.
            for listItem in index_dict: # For each list inside the index...
                loopInt = 1
                positionValue = 0
                for xy in listItem: # For each item inside each list...
                    positionValue += xy
                    if loopInt % round(time_per_bar/time_per_pos) == 0: # Check if the looping integer is divisible by a divison between the time per bar divided by the time gap between reports.
                        temp_list.append(positionValue)
                        positionValue = 0
                    loopInt += 1

                bar_values += [temp_list]
                temp_list = []

             # We also need a list for the other axis. That's where this next little loop comes in - it makes that list.

            xValues = []
            xValue = round(time_per_bar/time_per_pos)

            for things in bar_values[0]: # Makes a number of bars equal to the amount of data inputted.
                xValues.append(xValue)
                xValue += round(time_per_bar/time_per_pos) # The values for the bars are the same as the difference from before.

            useList = []
            highestValues = bar_values[0]
            rotator = 0

            # A little double for loop for creating a list of the highest values for each bar.
            # This is necessary because of the awkward way tkinter deals with stacked bar charts.

            for barList in bar_values:
                for item in barList:
                    if item > highestValues[rotator]:
                        highestValues[rotator] = item
                rotator = 0

            stackValue = 0;
            use = plt.bar(xValues,bar_values[0])
            useList.append(use)

            print(len(bar_values))

            while stackValue < len(bar_values)-1: # This section creates the actual graph.
                use = plt.bar(xValues,bar_values[stackValue+1], bottom = highestValues)
                useList.append(use)
                stackValue += 1

            plt.legend(useList,pos_meaning)
        else:
            print("The time period *must* be greater than the precision that the mouse is being tracked with!")

        return f, inner_plot

    def create_position_chart(self,f,coordsXY,vidSizeX,vidSizeY):
        inner_plot = f.add_subplot(1,1,1)

        realCoords = [[],[]]

        for item in coordsXY:
            realCoords[0].append(item[0])
            realCoords[1].append(item[1])

        plt.plot(realCoords[0], realCoords[1])

        axes = plt.gca()
        axes.set_xlim([0,vidSizeX]) # Create fixed size axis for my
        axes.set_ylim([0,vidSizeY])

        return f, inner_plot

    def estimate_poses_default(self,xSizes,ySizes,enteredCoords,vidSizeX,vidSizeY):
        coords = [[],[]]

        for item in enteredCoords:
            coords[0].append(item[0])
            coords[1].append(item[1])

        pos_list = [] # Used to contain the positions eventually.
        pos_meaning = {"Undefined":0,"Eating":1,"Moving":2,"Hanging":3,"Sleeping":4} # Used to store the relevant meaning of each integer in the final list.

        sizeRotate = 0 # Variable to keep track of the current frame.
        currentPosCount = 0 # Variable to define how long the mouse has been in it's current position.
        timeToSleep = 1200
        # Relevant because it takes 1200 frames (40 seconds) for a mouse to be classsed as asleep

        while sizeRotate < len(xSizes): # While the current frame is less than the frames in the x list... (Loop through the frames once)

            if xSizes[sizeRotate]*2 < ySizes[sizeRotate]: # If the mouse is more than twice as long as tall...
                pos_list.append(1)
            elif abs(coords[0][sizeRotate-20] - coords[0][sizeRotate]) >= 20 and abs(coords[1][sizeRotate-20] - coords[1][sizeRotate]) >= 20:
                # If the centre of the mouse is moving more than 20 pixels every 20 frames (1px/frame), then it is moving.
                pos_list.append(2)
            elif coords[1][sizeRotate] > vidSizeY/2:
                # If the mouse's centre of mass is higher than half the video width then the little lad must be hanging from the roof!!!
                pos_list.append(3)
            elif sizeRotate > timeToSleep: # If we're more than the time needed to sleep...
                if xSizes[sizeRotate] >= (ySizes[sizeRotate]*1.5) and abs(coords[0][sizeRotate-timeToSleep] - coords[0][sizeRotate]) < 30 and  abs(coords[1][sizeRotate-timeToSleep] - coords[1][sizeRotate]) < 30: # If the mouse is more than 1.5x as tall as long...
                    # If the difference between the central position of the mouse 20 frames ago and the central position of the mouse currently is less than 30 pixels in the x and y directions, then it hasn't moved very far and must be asleep.
                    # The mouse has to stay reasonably still for 1200 frames (within 30 px on x and y axis) to be classed as still in this system.
                    # Then it will be classed as asleep.
                    pos_list.append(4)
                else:
                    pos_list.append(0) # Undefined behaviour.

            else: # if we don't know what else to do...
                pos_list.append(0) #            ...it must be undefined.

            sizeRotate+=1


        return pos_meaning, pos_list