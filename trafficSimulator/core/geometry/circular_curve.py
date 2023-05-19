from .segment import Segment
import math

CURVE_RESOLUTION = 50


class CircularCurve(Segment):
    def __init__(self, center, radius, start_angle, end_angle):
        # Store characteristics
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

        # Generate path
        path = []
        for i in range(CURVE_RESOLUTION):
            t = self.start_angle + i / (CURVE_RESOLUTION - 1) * self.end_angle
            x = self.center[0] + self.radius * math.cos(t)
            y = self.center[1] + self.radius * math.sin(t)
            path.append((x, y))

        # Arc-length parametrization
        # TODO

        # Initialize super
        super().__init__(path)
