import lcm

from moteus_lcm import command_t

lc = lcm.LCM()

print("STARTING ECHO MOTOR_COMMAND SCRIPT...")

def handler(channel, data):
    msg = command_t.decode(data)

    text = f"POS: {msg.pos: 3.3f} VEL: {msg.vel: 3.3f} TOR: {msg.max_torque: 3.3f} STOP: {msg.stop_pos: 3.3f}"
    print(text)

sub = lc.subscribe("COMMAND", handler)


try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass
