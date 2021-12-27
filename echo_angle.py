import lcm

from AS5048A_lcm import angle_t
from moteus_lcm import query_t, command_t

lc = lcm.LCM()

print("STARTING ECHO ANGLE SCRIPT...")

def angle_handler(channel, data):
    msg = angle_t.decode(data)
    print(f"ANGLE MSG: {msg.angle: 3.3f}")

sub = lc.subscribe("ANGLE", angle_handler)


try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass
