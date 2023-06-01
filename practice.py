from random import random
import math
from trafficSimulator import *
from trafficSimulator.core.geometry.circular_curve import CircularCurve

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

# sim.create_circular_curve((0, 0), 100.0, 0, 2 * math.pi)

# for t in range(22):
#     vehicle = (0.1 * t, {'path': path, 'v': urb(5.0, 15.0), 'v_max': 120 * km / h,
#                'a_max': urb(0.3, 2.0), 'b_max': urb(1.5, 2.5), 'T': urb(0.8, 2.0),
#                          'T_res': 1.0, 's0': urb(2.0, 5.0)})
#     vehicles.append(vehicle)

# # vehicles.append((10.0, {'path': path, 'v': v, 'v_max': 50.0,
# #                         'a_max': 25.0, 'b_max': 10.0, 'T': 5.0}))

# vg = FiniteVehicleGenerator({
#     'vehicles': vehicles,
# })
# sim.add_vehicle_generator(vg)


cur = CircularCurve((0, 0), 50.0, 0, 2 * math.pi)

for i in range(21, -1, -1):
    vehicles.append(Vehicle(config={'id': i, 'path': path, 'v': urb(5.0, 15.0), 'v_max': 120 * km / h,
                                    'a_max': urb(0.3, 2.0), 'b_max': urb(1.5, 2.5), 'T': urb(0.8, 2.0),
                                    'T_res': 0.0, 's0': urb(2.0, 5.0), 'x': cur.get_length() * i / 22.0}))

sim.add_segment(cur)


for vehicle in vehicles:
    sim.add_vehicle_to_self(vehicle)
    cur.add_vehicle(vehicle)


win = Window(sim)
# win.run()
win.show()
