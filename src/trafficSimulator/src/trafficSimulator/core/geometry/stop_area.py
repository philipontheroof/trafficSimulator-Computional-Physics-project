from .segment import Segment


class StopArea(Segment):
    def __init__(self, vehicles_map, *args):
        super().__init__(*args)
        self.is_stop = False
        self.vehicles_map = vehicles_map
        self.stopped_vehicles = []

    def activate(self):
        # print("Stop area activated")
        for vehicle in self.vehicles:
            vehicle = self.vehicles_map[vehicle]
            vehicle.stop()
            self.stopped_vehicles.append(vehicle)
        self.is_stop = True

    def deactivate(self):
        # print("Stop area deactivated")
        for vehicle in self.stopped_vehicles:
            vehicle.go()
        self.stopped_vehicles = []
        self.is_stop = False
