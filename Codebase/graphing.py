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
        bar_values = []
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
            #index_dict = []
            temp_list = []

            # Next step is to turn the new binary lists into graphable values.
            for list_item in index_dict: # For each list inside the index...
                loop_int = 1
                position_value = 0
                for xy in list_item: # For each item inside each list...
                    position_value += xy
                    if loop_int % round(time_per_bar/time_per_pos) == 0: # Check if the looping integer is divisible by a divison between the time per bar divided by the time gap between reports.
                        temp_list.append(position_value)
                        position_value = 0
                    loop_int += 1
                bar_values += [temp_list]
                temp_list = []

             # We also need a list for the other axis. That's where this next little loop comes in - it makes that list.

            x_values = []
            x_value = round(time_per_bar/time_per_pos)

            for things in bar_values[0]: # Makes a number of bars equal to the amount of data inputted.
                x_values.append(x_value)
                x_value += round(time_per_bar/time_per_pos) # The values for the bars are the same as the difference from before.

            use_list = []
            highest_values = bar_values[0]
            rotator = 0

            # A little double for loop for creating a list of the highest values for each bar.
            # This is necessary because of the awkward way tkinter deals with stacked bar charts.

            for bar_list in bar_values:
                for item in bar_list:
                    if item > highest_values[rotator]:
                        highest_values[rotator] = item
                rotator = 0

            stack_value = 0;
            use = plt.bar(x_values,bar_values[0])
            use_list.append(use)

            print(len(bar_values))

            while stack_value < len(bar_values)-1: # This section creates the actual graph.
                use = plt.bar(x_values,bar_values[stack_value+1], bottom = highest_values)
                use_list.append(use)
                stack_value += 1

            plt.legend(use_list,pos_meaning)
        else:
            print("The time period *must* be greater than the precision that the mouse is being tracked with!")


        config_file = open("config.ini","r")
        config_lines = config_file.readlines()

        file_location = config_lines[2][13:]
        print(file_location)
        file_location = file_location.strip("\n")

        log_file = open(file_location+"/mousehub_data.log", "a+")

        print("Log file appended!")

        log_file.write("START OF FILE\n")

        for pos_item in pos_list:
            log_file.write(list(pos_meaning.keys())[list(pos_meaning.values()).index(pos_item)] + "\n")
            #print(list(pos_meaning.keys())[list(pos_meaning.values()).index(pos_item)])

        log_file.write("END OF FILE\n")

        return f, inner_plot

    def create_position_chart(self,f,coords_xy,vid_size_x,vid_size_y):
        inner_plot = f.add_subplot(1,1,1)

        real_coords = [[],[]]

        for item in coords_xy:
            real_coords[0].append(item[0])
            real_coords[1].append(item[1])

        plt.plot(real_coords[0], real_coords[1])

        axes = plt.gca()
        axes.set_xlim([0,vid_size_x]) # Create fixed size axis for my
        axes.set_ylim([0,vid_size_y])

        return f, inner_plot

    def estimate_poses_default(self,x_sizes,y_sizes,entered_coords,vid_size_x,vid_size_y):
        coords = [[],[]]

        for item in entered_coords:
            coords[0].append(item[0])
            coords[1].append(item[1])

        pos_list = [] # Used to contain the positions eventually.
        pos_meaning = {"Undefined":0,"Eating":1,"Moving":2,"Hanging":3,"Sleeping":4} # Used to store the relevant meaning of each integer in the final list.

        size_rotate = 0 # Variable to keep track of the current frame.
        current_pos_count = 0 # Variable to define how long the mouse has been in it's current position.
        time_to_sleep = 1200
        # Relevant because it takes 1200 frames (40 seconds) for a mouse to be classsed as asleep

        while size_rotate < len(x_sizes): # While the current frame is less than the frames in the x list... (Loop through the frames once)

            if x_sizes[size_rotate]*2 < y_sizes[size_rotate]: # If the mouse is more than twice as long as tall...
                pos_list.append(1)
            elif abs(coords[0][size_rotate-20] - coords[0][size_rotate]) >= 20 and abs(coords[1][size_rotate-20] - coords[1][size_rotate]) >= 20:
                # If the centre of the mouse is moving more than 20 pixels every 20 frames (1px/frame), then it is moving.
                pos_list.append(2)
            elif coords[1][size_rotate] > vid_size_y/2:
                # If the mouse's centre of mass is higher than half the video width then the little lad must be hanging from the roof!!!
                pos_list.append(3)
            elif size_rotate > time_to_sleep: # If we're more than the time needed to sleep...
                if x_sizes[size_rotate] >= (y_sizes[size_rotate]*1.5) and abs(coords[0][size_rotate-time_to_sleep] - coords[0][size_rotate]) < 30 and  abs(coords[1][size_rotate-time_to_sleep] - coords[1][size_rotate]) < 30: # If the mouse is more than 1.5x as tall as long...
                    # If the difference between the central position of the mouse 20 frames ago and the central position of the mouse currently is less than 30 pixels in the x and y directions, then it hasn't moved very far and must be asleep.
                    # The mouse has to stay reasonably still for 1200 frames (within 30 px on x and y axis) to be classed as still in this system.
                    # Then it will be classed as asleep.
                    pos_list.append(4)
                else:
                    pos_list.append(0) # Undefined behaviour.

            else: # if we don't know what else to do...
                pos_list.append(0) #            ...it must be undefined.

            size_rotate+=1


        return pos_meaning, pos_list
