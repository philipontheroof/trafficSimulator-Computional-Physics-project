from random import random, seed as random_seed
import math
from trafficSimulator import *
from trafficSimulator.core.geometry.circular_curve import CircularCurve
import numpy as np

sim = Simulation()

lane_space = 3.5
intersection_size = 12
length = 100

radius = 50.0
stop_area_length = 5.0

# sim.create_quadratic_bezier_curve(
#     (radius, stop_area_length), (radius, radius), (0, radius))
# sim.create_quadratic_bezier_curve((0, radius), (-radius, radius), (-radius, 0))
# sim.create_quadratic_bezier_curve(
#     (-radius, 0), (-radius, -radius), (0, -radius))
# sim.create_quadratic_bezier_curve((0, -radius), (radius, -radius), (radius, 0))
# sim.create_stop_area((radius, 0), (radius, stop_area_length))


def urb(a, b):
    return random() * (b - a) + a


path = [0,] * 100

vehicles = []

km = 1000
h = 3600

cur = CircularCurve((0, 0), 50.0, 0, 2 * math.pi)

random_seed(0)

N = 22
for i in range(N - 1, -1, -1):
    x = cur.get_length() * i / N + np.random.uniform(-3.0, 3.0)
    if x < 0:
        x = 0
    vehicles.append(Vehicle(
        config={'id': i, 'path': path, 'v': urb(5.0, 15.0), 'v_max': 120 * km / h,
                'a_max': 4.0, 'b_max': 8.0, 'T': 1.3,
                'T_res': 0.5, 's0': 3.0, 'x': cur.get_length() * i / N}))

sim.add_segment(cur)


for vehicle in vehicles:
    sim.add_vehicle_to_self(vehicle)
    cur.add_vehicle(vehicle)


win = Window(sim)
# win.run()
win.show()
