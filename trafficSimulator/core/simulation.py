from .geometry.circular_curve import CircularCurve
from .geometry.stop_area import StopArea
from .vehicle_generator import VehicleGenerator
from .geometry.quadratic_curve import QuadraticCurve
from .geometry.cubic_curve import CubicCurve
from .geometry.segment import Segment
from .vehicle import Vehicle


class Simulation:
    def __init__(self):
        self.segments = []
        self.vehicles = {}
        self.vehicle_generator = []

        self.t = 0.0
        self.frame_count = 0
        self.dt = 1 / 60

        self.stop_areas = []
        self.is_stop = False
        print('imported')

    def add_vehicle(self, veh):
        self.vehicles[veh.id] = veh
        if len(veh.path) > 0:
            self.segments[veh.path[0]].add_vehicle(veh)

    def add_segment(self, seg):
        self.segments.append(seg)

    def add_stop_area(self, stop_area):
        self.stop_areas.append(stop_area)
        self.segments.append(stop_area)

    def add_vehicle_generator(self, gen):
        self.vehicle_generator.append(gen)

    def create_vehicle(self, **kwargs):
        veh = Vehicle(kwargs)
        self.add_vehicle(veh)

    def create_segment(self, *args):
        seg = Segment(args)
        self.add_segment(seg)

    def create_stop_area(self, *args):
        seg = StopArea(self.vehicles, args)
        self.add_stop_area(seg)

    def create_quadratic_bezier_curve(self, start, control, end):
        cur = QuadraticCurve(start, control, end)
        self.add_segment(cur)

    def create_circular_curve(self, center, radius, start_angle, end_angle):
        cur = CircularCurve(center, radius, start_angle, end_angle)
        self.add_segment(cur)

    def create_cubic_bezier_curve(self, start, control_1, control_2, end):
        cur = CubicCurve(start, control_1, control_2, end)
        self.add_segment(cur)

    def create_vehicle_generator(self, **kwargs):
        gen = VehicleGenerator(kwargs)
        self.add_vehicle_generator(gen)

    def run(self, steps):
        for _ in range(steps):
            self.update()

    def update(self):

        # Update vehicles
        for segment in self.segments:
            if len(segment.vehicles) != 0:
                vehicle = self.vehicles[segment.vehicles[0]]
                leading_vehicle, lead_x = self.find_leading_vehicle(vehicle)
                # print(
                #     f'found outside: {str(vehicle.id)[-2:]} follows {str(leading_vehicle.id)[-2:]}, lead_x: {lead_x}')

                vehicle.update_outside(leading_vehicle, self.dt, lead_x)
            for i in range(1, len(segment.vehicles)):
                # print(
                #     f'found inside: {str(segment.vehicles[i])[-2:]} follows {str(segment.vehicles[i-1])[-2:]}')
                self.vehicles[segment.vehicles[i]].update(
                    self.vehicles[segment.vehicles[i - 1]], self.dt)

        # Check roads for out of bounds vehicle
        for segment in self.segments:
            # If road has no vehicles, continue
            if len(segment.vehicles) == 0:
                continue
            # If not
            vehicle_id = segment.vehicles[0]
            vehicle = self.vehicles[vehicle_id]
            # If first vehicle is out of road bounds
            if vehicle.x >= segment.get_length():
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.segments[next_road_index].vehicles.append(vehicle_id)
                    # Reset vehicle properties
                    vehicle.x = 0
                    # In all cases, remove it from its road
                    segment.vehicles.popleft()
                else:
                    # If not, remove it from the road
                    segment.vehicles.popleft()
                    # And remove it from the simulation
                    del self.vehicles[vehicle_id]

        # Update vehicle generators
        for gen in self.vehicle_generator:
            gen.update(self)
        # Increment time
        self.t += self.dt
        self.frame_count += 1

    def find_leading_vehicle(self, vehicle):
        if vehicle.current_road_index >= len(vehicle.path) - 1:
            return None, None

        current_road = self.segments[vehicle.path[vehicle.current_road_index]]
        road_indices_ahead = vehicle.path[vehicle.current_road_index + 1:]
        lead_x = current_road.get_length() - vehicle.x

        for road_index in road_indices_ahead:
            if len(self.segments[road_index].vehicles) > 0:
                leading_vehicle = self.vehicles[self.segments[road_index].vehicles[-1]]
                lead_x += leading_vehicle.x
                return leading_vehicle, lead_x
            else:
                lead_x += self.segments[road_index].get_length()
        return None, None

    def activate_stop(self):
        for stop_area in self.stop_areas:
            stop_area.activate()

    def deactivate_stop(self):
        for stop_area in self.stop_areas:
            stop_area.deactivate()
