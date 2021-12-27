import lcm
import logging
import time
from AS5048A_lcm import angle_t
from moteus_lcm import command_t

logging.basicConfig(
        filename="log.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format='%(asctime)s %(message)s')


class Logg:
    def __init__(self):

        self.lc = lcm.LCM()

        self.lc.subscribe("ANGLE", self.angle_handler)
        self.lc.subscribe("COMMAND", self.command_handler)

        self.angle_started = False
        self.command_started = False

        self.counter = 0;

        return

    def angle_handler(self, channel, data):
        
        self.angle_started = True
        msg = angle_t.decode(data)
        self.last_angle = msg.angle
        
    def command_handler(self, channel, data):
        self.command_started = True
        msg = command_t.decode(data)
        self.last_cmd = msg.pos


    def loop(self):
        self.lc.handle_timeout(1)
        if self.angle_started and self.command_started:
            logging.debug(f"{self.last_angle}, {self.last_cmd}")
            self.counter = self.counter + 1
            print(self.counter)
    
    def run(self):
        while self.counter < 2000:
            start = time.time_ns()
            self.loop()
            end = time.time_ns()
            time.sleep(max(0, 0.01 - 1e-9 *  (end - start)))
            


l = Logg()
l.run()
