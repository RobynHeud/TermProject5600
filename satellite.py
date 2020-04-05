import sys
import numpy as np
import helper_functions as helper
import math


# Make a list of satellites, with their initial starting positions
class Satellite:
    """
    A representation for a Satellite with a label (id number) sending a signal (x, y, z) at time t
    """

    def __init__(self, label, u_1=0, u_2=0, u_3=0, v_1=0, v_2=0, v_3=0, theta=0):
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


# List of satellites in orbit
sat_list = list()

# Get satellite details from data.dat file and populate the satellite list
with open("all/data.dat", "r") as data:
    sat_num = 0
    new_sat = Satellite(sat_num)

    for idx, line in enumerate(data):
        index = idx % 7
        line_info = line.strip().split("/=")

        if index == 0:
            new_sat.u_1 = float(line_info[0])
        elif index == 1:
            new_sat.u_2 = float(line_info[0])
        elif index == 2:
            new_sat.u_3 = float(line_info[0])
        elif index == 3:
            new_sat.v_1 = float(line_info[0])
        elif index == 4:
            new_sat.v_2 = float(line_info[0])
        elif index == 5:
            new_sat.v_3 = float(line_info[0])
        elif index == 6:
            new_sat.theta = float(line_info[0])
            sat_list.append(new_sat)
            sat_num += 1
            new_sat = Satellite(sat_num)

# Creates and writes to log file
with open("Satellite.log", "w") as log:
    log.write("Satellite Log, Jess Campbell, Austin Watkins, Carlos Guerra\n")
    log.write("\nSimulation Details:\n")

    log.write("pi = " + str(math.pi))
    log.write("\nspeed of light = " + str(helper.c))
    log.write("\nradius of earth = " + str(helper.R))
    log.write("\nsidereal day = " + str(helper.s))
    log.write("\nsatellite period = " + str(helper.p))
    log.write("\nsatellite altitude = " + str(helper.h))

    # Log the satellite info
    for sat in sat_list:
        log.write("\n\nSatellite " + str(sat.label) + ":")
        log.write("\nu = [" + str(sat.u_1) + ", " + str(sat.u_2) + ", " + str(sat.u_3) + "]")
        log.write("\nv = [" + str(sat.v_1) + ", " + str(sat.v_2) + ", " + str(sat.v_3) + "]")
        log.write("\ntheta = " + str(sat.theta))

    # Take in line with timestamp, latitude (3 parts), NS, longitude (3 parts), EW, and height
    for epoch, line in enumerate(sys.stdin):
        log.write("\nEpoch = {epoch_numb}".format(epoch_numb=epoch))
        log.write("\nInput: {info}".format(info=line))

        # Parse the string and convert to Float64
        line_array = line.split()
        value_array = []
        for elm in line_array:
            new_elm = float(elm)
            value_array.append(new_elm)

        # Translate to Cartesian coordinates with rotation
        cart_coords = helper.polar_to_cart(*value_array)

        # vehicle timestamp
        t_v = value_array[0]

        # Use new coordinates to determine what satellites are in view/above the horizon
        sat_in_view = []
        for sat in sat_list:
            sat_position = np.array(sat.get_curr_position(t_v))
            if helper.above_horizon(*cart_coords, sat_position[0], sat_position[1], sat_position[2]):
                sat_in_view.append(sat)

        # Find the timestamp for each satellite
        log.write("\nOutput:")
        for sat in sat_in_view:
            # set current to the vehicle timestamp to start
            last_ts = t_v
            done = False
            while not done:
                current_ts = t_v - np.linalg.norm(sat.get_curr_position(last_ts) - cart_coords) / helper.c
                if abs(current_ts - last_ts) < 0.01 / helper.c:
                    done = True
                last_ts = current_ts

            sat_position = np.array(sat.get_curr_position(current_ts))
            log.write("\n{Sat_Num} {Time_Curr} {Sat_Pos_1} {Sat_Pos_2} {Sat_Pos_3}".format(Sat_Num=sat.label,
                                                                                           Time_Curr=current_ts,
                                                                                           Sat_Pos_1=sat_position[0],
                                                                                           Sat_Pos_2=sat_position[1],
                                                                                           Sat_Pos_3=sat_position[2]))
            print(sat.label, current_ts, sat_position[0], sat_position[1], sat_position[2])
