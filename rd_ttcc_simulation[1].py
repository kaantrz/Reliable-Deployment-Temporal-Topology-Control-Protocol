import random
import time
from collections import deque

class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.active = False

    def activate(self):
        # activation process
        time.sleep(random.uniform(0.1, 0.3))
        self.active = True
        print(f"Sensor {self.sensor_id} activated.")

    def deactivate(self):
        #  deactivation process
        time.sleep(random.uniform(0.1, 0.3))
        self.active = False
        print(f"Sensor {self.sensor_id} deactivated.")

    def send_heartbeat(self):
        if self.active:
            #  sending heartbeat message
            time.sleep(random.uniform(0.1, 0.2))
            print(f"Heartbeat from sensor {self.sensor_id}.")
            return True
        else:
            return False

class BossNode:
    def __init__(self, sensors, covers):
        self.sensors = sensors
        self.covers = deque(covers)
        self.active_cover = []

    def activate_next_cover(self):
        if self.active_cover:
            for sensor in self.active_cover:
                sensor.deactivate()
        
        if self.covers:
            self.active_cover = self.covers.popleft()
            print("Activating new cover:")
            for sensor in self.active_cover:
                sensor.activate()
        else:
            print("No more covers to activate. Network coverage is lost.")

    def check_heartbeats(self):
        print("Checking heartbeats...")
        all_heartbeats_received = True
        for sensor in self.active_cover:
            if not sensor.send_heartbeat():
                all_heartbeats_received = False
                print(f"Sensor {sensor.sensor_id} failed to send heartbeat.")
        
        if not all_heartbeats_received:
            print("Failure detected. Switching to next cover.")
            self.activate_next_cover()

    def simulate(self, intervals):
        print("Starting RD-TTCP simulation...")
        self.activate_next_cover()
        for _ in range(intervals):
            time.sleep(5)  # Simulate listening period
            self.check_heartbeats()
            time.sleep(1)  # Simulate interval between checks


sensors = [Sensor(i) for i in range(5)]


covers = [
    [sensors[0], sensors[1]],  # Cover 1
    [sensors[2], sensors[3]],  # Cover 2
    [sensors[4]]               # Cover 3
]


boss_node = BossNode(sensors, covers)


boss_node.simulate(3)
