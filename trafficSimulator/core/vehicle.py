import uuid
import numpy as np
from collections import deque


class Vehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        self.id = uuid.uuid4()
        self.dt = 1 / 60

        self.T_res = 0.7
        self.records = deque([], maxlen=int(self.T_res / self.dt))

        self.l = 3.6
        self.s0 = 10.0
        self.T = 1
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = 0
        self.a = 0
        self.stopped = False

    def init_properties(self):
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2

        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T * self.v +
                     delta_v * self.v / self.sqrt_ab)) / delta_x

        a = self.a_max * (1 - (self.v / self.v_max)**4 - alpha**2)
        self.records.append(a)
        self.a = self.records[0]

        if self.stopped:
            self.a = -self.b_max * self.v / self.v_max

    def update_outside(self, lead, dt, lead_x):
        # Update position and velocity
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2

        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead_x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T * self.v +
                     delta_v * self.v / self.sqrt_ab)) / delta_x

        a = self.a_max * (1 - (self.v / self.v_max)**4 - alpha**2)
        self.records.append(a)
        self.a = self.records[0]

        if self.stopped:
            self.a = -self.b_max * self.v / self.v_max

    def stop(self):
        print(f'Vehicle {str(self.id)[-2:]} stopping')
        self.stopped = True

    def go(self):
        print(f'Vehicle {str(self.id)[-2:]} going')
        self.stopped = False
