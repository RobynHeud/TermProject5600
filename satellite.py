import sys
import helper_functions as helper
import numpy as np
import scipy.constants
import logging
import os
from decimal import *
import helper_functions as helper
import math

# Make a list of satellites, with their initial starting positions
class Satellite:
    """
    A representation for a Satellite with a label (id number) sending a signal (x, y, z) at time t
    """

    def __init__(self, label, u_1, u_2, u_3, v_1, v_2, v_3, theta):
        self.label = int(label)
        self.u_1 = u_1
        self.u_2 = u_2
        self.u_3 = u_3
        self.v_1 = v_1
        self.v_2 = v_2
        self.v_3 = v_3
        self.theta = theta

    def __repr__(self):
        return f'({self.label})'

    def get_curr_position(self, ts):
        height = helper.R + helper.h
        inner_value = 2 * math.pi * ts / helper.p + self.theta
        u = np.array([self.u_1, self.u_2, self.u_3])
        v = np.array([self.v_1, self.v_2, self.v_3])
        return height * (math.cos(inner_value) * u + math.sin(inner_value) * v)

# Data from data.dat file
u = [[0 for x in range(3)] for y in range(24)]
v = [[0 for x in range(3)] for y in range(24)]
period = [0 for x in range(24)]
altitude = [0 for x in range(24)]
phase = [0 for x in range(24)]
sat_list = list()

# Creates and writes to log file
with open("Satellite.log", "w") as log:
    log.write("Satellite Log, Jess Campbell, Austin Watkins, Carlos Guerra\n")
    log.write("\n  data.dat: \n\n")

    # Writes/Reads information from data.dat
    with open("all/data.dat", "r") as data:
        SatNumb = 0
        index = 0
        for line in data:
            line_info = line.split("/=")

            tempIndex = (index - 4) % 9

            if tempIndex == 0 or tempIndex == 1 or tempIndex == 2:
                u[SatNumb][tempIndex] = float(line_info[0])
                log.write("u[{Sat}][{Index}] = {Info}\n".format(Sat=SatNumb, Index=tempIndex, Info=line_info[0]))
                index = index + 1
            elif tempIndex == 3 or tempIndex == 4 or tempIndex == 5:
                v[SatNumb][tempIndex % 3] = line_info[0]
                log.write(
                    "v[{Sat}][{Index}] = {Info}\n".format(Sat=SatNumb, Index=(tempIndex % 3), Info=line_info[0]))
                index = index + 1
            elif tempIndex == 8:
                phase[SatNumb] = line_info[0]
                log.write("phase[{Sat}] = {Info}\n".format(Sat=SatNumb, Info=line_info[0]))
                index = index + 1
                SatNumb = SatNumb + 1
            else:
                continue
        epoch = 0
        # Take in line with timestamp, latitude (3 parts), NS, longitude (3 parts), EW, and height
        for line in sys.stdin:
            log.write(" --- epoch = {epoch_numb}\n".format(epoch_numb = epoch))
            log.write("read {info}\n".format(info = line))
            # Parse the string and convert to Float64
            line_array = line.split()
            value_array = []
            for elm in line_array:
                new_elm = float(elm)
                value_array.append(new_elm)

            # Translate to Cartesian coordinates with rotation
            cart_coords = helper.polar_to_cart(*value_array)
            print(cart_coords)

            t_v = value_array[0]
            # Use new coordinates to determine what satellites are in view/above the horizon
            sat_in_view = []
            for sat in sat_list:
                sat_position = np.array(sat.get_curr_position(t_v))
                if helper.above_horizon(*cart_coords, sat_position[0][0], sat_position[0][1], sat_position[0][2]):
                    sat_in_view.append(sat)

            log.write("Wrote:\n")
            for sat in sat_in_view:
                done = False
                current = t_v
                while not done:                    
                    next = t_v - np.linalg.norm(sat.get_curr_position(current)-cart_coords)/helper.c
                    if abs(next-current) < Decimal(0.01/helper.c):
                        done = True
                    current = next

                sat_position = np.array(sat.get_curr_position(current))
                log.write("{Sat_Num} {Time_Curr} {Sat_Pos_1} {Sat_Pos_2} {Sat_Pos_3}".format(Sat_Num = sat, Time_Curr = current, Sat_Pos_1 = sat_position[0][0], Sat_Pos_2 = sat_position[0][1], Sat_Pos_3 = sat_position[0][2]))
                # print(sat, current, sat_position[0][0], sat_position[0][1], sat_position[0][2])
            epoch += 1
            print("yep")
            # Output index, timestamp, and cartesian coordinate location to stdout
