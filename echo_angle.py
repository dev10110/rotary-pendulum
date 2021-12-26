import lcm

from AS5048A_lcm import angle_t
from moteus_lcm import query_t, command_t

lc = lcm.LCM()

print("STARTING ECHO ANGLE SCRIPT...")

def angle_handler(channel, data):
    msg = angle_t.decode(data)
    print("ANGLE MSG: %.3f" % msg.angle)

sub = lc.subscribe("ANGLE", angle_handler)


try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass
