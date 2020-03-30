import sys

from collections import defaultdict
from math import sqrt
from typing import List

import numpy as np

import helper_functions as help


class Satellite:
    """
    A representation for a Satellite with a label (id number) sending a signal (x, y, z) at time t

    """

    def __init__(self, label, t, x, y, z):
        self.label = int(label)
        self.t = t
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.label}, {self.t}, {self.x}, {self.y}, {self.z})'


class Vehicle:
    """
    A representation for the vehicle.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


def distance(V, S):
    return sqrt((V.x - S.x) ** 2 + (V.y - S.y) ** 2 + (V.z - S.z) ** 2)


def solve_location(satellites: List[Satellite]):
    """
    Solve the non linear system of equations.

    :param satellites:
    :return:
    """

    # At SLC:
    V = Vehicle(-1795225.28989696, -4477174.36119832, 4158593.45315397)

    for _ in range(5000):

        satellite_by_two = []
        for i in range(0, len(satellites) - 1):
            satellite_by_two.append(satellites[i:i + 2])

        F = []
        matrix = []
        for s1, s2 in satellite_by_two:
            row = []
            for var in ['x', 'y', 'z']:
                matrix_element = eval(f'V.{var} - s1.{var}') / distance(V, s1) - \
                                 eval(f'V.{var} - s2.{var}') / distance(V, s2)
                row.append(matrix_element)
            matrix.append(row)

            # fixme: import speed of light
            F.append(distance(V, s1) - distance(V, s2) - 299792458 * (s2.t - s1.t))

        jacobian = np.array(matrix)
        s = np.array(F)
        # todo: build linear solver ourselves (??)
        sol = np.linalg.solve(jacobian.T @ jacobian, -jacobian.T @ s)
        V.x += sol[0]
        V.y += sol[1]
        V.z += sol[2]
    return V


satellites = []
# todo : modify for "production" (by commenting out)
# for line in sys.stdin:
for line in open('all/b12_input.txt'):
    # Parse the string and convert to Float64
    satellite_values = list(map(float, line.split()))
    label = satellite_values[0]
    satellites.append(Satellite(*satellite_values))

# todo: talk about this method with team
satellite_for_t = defaultdict(list)
for s in satellites:
    satellite_for_t[int(s.t)].append(s)

satellite_for_t = sorted(satellite_for_t.items(), key=lambda x: x[0])
satellite_for_t = [s for (t, s) in satellite_for_t]
for group_satellite in satellite_for_t:
    sol = solve_location(group_satellite)
    polar = help.cart_to_polar(0, sol.x, sol.y, sol.z)
    print(polar)

