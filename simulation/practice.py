from trafficSimulator import *
from random import random

sim = Simulation()

lane_space = 3.5
intersection_size = 12
length = 100

radius = 50.0
stop_area_length = 5.0

sim.create_quadratic_bezier_curve(
    (radius, stop_area_length), (radius, radius), (0, radius))
sim.create_quadratic_bezier_curve((0, radius), (-radius, radius), (-radius, 0))
sim.create_quadratic_bezier_curve(
    (-radius, 0), (-radius, -radius), (0, -radius))
sim.create_quadratic_bezier_curve((0, -radius), (radius, -radius), (radius, 0))
sim.create_stop_area((radius, 0), (radius, stop_area_length))

path = [0, 1, 2, 3, 4] * 100

vehicles = []

for t in range(30):
    v = random()*13 + 3
    vehicle = (0.5*t, {'path': path, 'v': v, 'v_max': 50.0,
               'a_max': 5.0, 'b_max': 2.5, 'T': 1.0})
    vehicles.append(vehicle)

# vehicles.append((10.0, {'path': path, 'v': v, 'v_max': 50.0,
#                         'a_max': 25.0, 'b_max': 10.0, 'T': 5.0}))

vg = FiniteVehicleGenerator({
    'vehicles': vehicles,
})
sim.add_vehicle_generator(vg)


win = Window(sim)
# win.run()
win.show()
