import sys
import helper_functions as help
import numpy as np
import scipy
import logging
import os
from decimal import *

# Radius of the Earth
R = 6367444.50 # meters
# Sidereal Day
s = 86164.09 # seconds
# Satellite Height
h = 20200200 # meters
# Satellite Orbital Period
p = s / 2

#Data from data.dat file 
u = [[0 for x in range(3)]for y in range(24)]
v = [[0 for x in range(3)] for y in range(24)]
period = [0 for x in range(24)]
altitude = [0 for x in range(24)]
phase = [0 for x in range(24)]

with open("Satellite.log", "w") as log:
    log.write("Satellite Log, Jess Campbell, Austin Watkins, Carlos Guerra\n")
    log.write("\n  data.dat: \n\n")

    #Writes/Reads information from data.dat
    with open("data.dat", "r") as data:
        SatNumb = 0
        index = 0
        for line in data:
            line_info = line.split("/=")
            #Reads in Pi
            if(index == 0):
                pi = Decimal(line_info[0])
                log.write("pi = {}\n".format(pi))
                index = index + 1

            #Reads in C
            elif(index == 1):
                c = Decimal(line_info[0])
                log.write("c = {}\n".format(c))
                index = index + 1

            #Reads in R
            elif(index == 2):
                R = Decimal(line_info[0])
                log.write("R = {}\n".format(R))
                index = index + 1

            #Reads in the value for s
            elif(index == 3):
                s = Decimal(line_info[0])
                log.write("s = {}\n".format(s))
                index = index + 1

            else:
                tempIndex = (index - 4) % 9

                if(tempIndex == 0 or tempIndex == 1 or tempIndex == 2):
                    u[SatNumb][tempIndex] = float(line_info[0])
                    log.write("u[{Sat}][{Index}] = {Info}\n".format(Sat = SatNumb, Index = tempIndex, Info = line_info[0]))
                    index = index + 1
                elif(tempIndex == 3 or tempIndex == 4 or tempIndex == 5):
                    v[SatNumb][tempIndex % 3] = line_info[0]
                    log.write("v[{Sat}][{Index}] = {Info}\n".format(Sat = SatNumb, Index = (tempIndex % 3), Info = line_info[0]))
                    index = index + 1
                elif(tempIndex == 6):
                    period[SatNumb] =line_info[0]
                    log.write("period[{Sat}] = {Info}\n".format(Sat = SatNumb, Info = line_info[0]))
                    index = index + 1
                elif(tempIndex == 7):
                    altitude[SatNumb] = line_info[0]
                    log.write("altitude[{Sat}] = {Info}\n".format(Sat = SatNumb, Info = line_info[0]))
                    index = index + 1
                elif(tempIndex == 8):
                    phase[SatNumb] = line_info[0]
                    log.write("phase[{Sat}] = {Info}\n".format(Sat = SatNumb, Info = line_info[0]))
                    index = index + 1
                    SatNumb = SatNumb + 1
                else:
                    print("here")

        print(u)


    log.write("\n")

    print(R)
    print(pi)
    print(c)
    print(s)

    # Take in line with timestamp, latitude (3 parts), NS, longitude (3 parts), EW, and height
    # for line in sys.stdin:
    #     log.write(line)

    #     # Parse the string and convert to Float64
    #     line_array = line.split()
    #     value_array = []
    #     for elm in line_array:
    #         new_elm = float(elm)
    #         value_array.append(new_elm)

    #     # Translate to Cartesian coordinates with rotation
    #     cart_coords = help.polar_to_cart(*value_array)
    #     print(cart_coords)

        # Use new coordinates to determine what satellites are in view/above the horizon
    

        # Output index, timestamp, and cartesian coordinate location to stdout
