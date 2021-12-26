import lcm

from moteus_lcm import motor_state_t

lc = lcm.LCM()

print("STARTING ECHO MOTOR_STATE SCRIPT...")

def handler(channel, data):
    msg = motor_state_t.decode(data)

    text = f"MODE: {msg.mode}  POS: {msg.position: 3.3f} VEL: {msg.velocity: 3.3f} TOR: {msg.torque: 3.3f} VOLT: {msg.voltage:3.3f} FAULT: {msg.fault}"
    print(text)

sub = lc.subscribe("MOTOR_STATE", handler)


try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass
