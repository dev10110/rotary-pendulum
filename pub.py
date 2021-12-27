import lcm
import random
import numpy as np
from moteus_lcm import command_t
import sys

if len(sys.argv) == 1:
    pos = 0.0
else:
    pos = float(sys.argv[1])
    print(pos)

lc = lcm.LCM()

msg = command_t()
msg.pos = pos 
msg.stop_pos = 0.0
msg.vel = 5.0
msg.max_torque = 2.0

lc.publish("COMMAND", msg.encode())
