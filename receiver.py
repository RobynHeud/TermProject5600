import sys
from collections import defaultdict
from math import sqrt
from typing import List
import numpy as np
import helper_functions as helper


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


def solve_location(sats: List[Satellite]):
    """
    Solve the non linear system of equations.

    :param sats:
    :return:
    """

    # At SLC:
    V = Vehicle(0, 0, helper.R)

    done = False
    while not done:
        satellite_by_two = []

        for i in range(0, len(sats) - 1):
            satellite_by_two.append(sats[i:i + 2])

        F = []
        matrix = []
        for s1, s2 in satellite_by_two:
            row = []
            for var in ['x', 'y', 'z']:
                matrix_element = eval(f'V.{var} - s1.{var}') / distance(V, s1) - \
                                 eval(f'V.{var} - s2.{var}') / distance(V, s2)
                row.append(matrix_element)
            matrix.append(row)

            F.append(distance(V, s1) - distance(V, s2) - helper.c * (s2.t - s1.t))

        jacobian = np.array(matrix)
        s = np.array(F)

        sol = np.linalg.solve(jacobian.T @ jacobian, -jacobian.T @ s)
        V.x += sol[0]
        V.y += sol[1]
        V.z += sol[2]

        # print(sol)
        done = np.linalg.norm(sol) < 1 / 1000000

    t_v = (distance(V, sats[0]) + helper.c * sats[0].t) / helper.c
    return V, t_v


satellites = []
for line in sys.stdin:
    # Parse the string and convert to Float64
    satellite_values = list(map(float, line.split()))
    label = satellite_values[0]
    satellites.append(Satellite(*satellite_values))

# todo: talk about this method with team (send email to prof.)
satellite_for_t = defaultdict(list)
for s in satellites:
    satellite_for_t[int(s.t)].append(s)

satellite_for_t = sorted(satellite_for_t.items(), key=lambda x: x[0])
satellite_for_t = [s for (t, s) in satellite_for_t]
for group_satellite in satellite_for_t:
    sol, t = solve_location(group_satellite)
    polar = helper.cart_to_polar(t, sol.x, sol.y, sol.z)
    print(*polar)
