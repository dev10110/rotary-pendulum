import lcm
import random
import numpy as np
from moteus_lcm import command_t

lc = lcm.LCM()

msg = command_t()
msg.pos = -2.0 
msg.stop_pos = 0.0
msg.vel = 5.0
msg.max_torque = 2.0

lc.publish("COMMAND", msg.encode())
