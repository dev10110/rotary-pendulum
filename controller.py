import lcm
import random
import numpy as np
import time

from moteus_lcm import command_t, motor_state_t
from AS5048A_lcm import angle_t

class Controller:
    def __init__(self):
        self.RATE = 0.01  # in seconds
        self.lc = lcm.LCM()

        # create subscribers
        self.lc.subscribe("ANGLE", self.angle_handler)
        self.lc.subscribe("MOTOR_STATE", self.motor_state_handler)
        
        self.angle_rec = False
        self.motor_state_rec = False
        self.started = False

    def angle_handler(self, channel, data):
        msg = angle_t.decode(data)
        self.angle = msg.angle
        self.angle_rec = True


    def motor_state_handler(self, channel, data):
        msg = motor_state_t.decode(data)
        self.current_pos = msg.position
        self.motor_state_rec = True

    def update_target(self):

        k = -1/360.0

        self.target_pos = k * (180 - self.angle)

    def loop(self):
        # this is the sequence to run each time
        # collect info from subscribers
        self.lc.handle_timeout(1)
        
        # check if ready to start control
        if self.started == False:
            self.started = self.angle_rec & self.motor_state_rec
        
        if self.started == False:
            return

        # calculate target message
        self.update_target()

        # publish target 
        self.publish_target()
        
    def run(self):
        while True: 
            start_time = time.time_ns()
            self.loop()
            end_time = time.time_ns()
            time.sleep(max(0.0, self.RATE - 1e-9 * (end_time - start_time)))

    def publish_target(self):
        msg = command_t()
        msg.pos = 0.8*self.current_pos + 0.2*self.target_pos
        msg.vel = 5.0
        msg.max_torque = 2.0
        msg.stop_pos = 0.0#self.target_pos

        self.lc.publish("COMMAND", msg.encode())

if __name__ == "__main__":

    controller = Controller()
    controller.run()

