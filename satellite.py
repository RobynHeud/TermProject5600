import sys
import helper_functions as help
import numpy as np

# Radius of the Earth
R = 6367444.50 # meters
# Sidereal Day
s = 86164.09 # seconds
# Satellite Height
h = 20200200 # meters
# Satellite Orbital Period
p = s / 2

# Take in line with timestamp, latitude (3 parts), NS, longitude (3 parts), EW, and height
for input in sys.stdin:
    # Parse the string and convert to Float64
    input_array = input.split()
    value_array = []
    for elm in input_array:
        new_elm = float(elm)
        value_array.append(new_elm)


    # Translate to Cartesian coordinates with rotation
    cart_coords = help.polar_to_cart(*value_array)
    print(cart_coords)
    polar_coords = help.cart_to_polar(0, *cart_coords)
    print(polar_coords)

    # Use new coordinates to determine what satellites are in view/above the horizon


    # Output index, timestamp, and cartesian coordinate location to stdout
