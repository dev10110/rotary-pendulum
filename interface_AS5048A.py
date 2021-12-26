import spidev
import lcm
from AS5048A_lcm import angle_t

spi = spidev.SpiDev()
spi.open(0,0)

spi.mode = 0x01

lc = lcm.LCM()

print("STARTING AS5048A READER")

def wrap(a):

    if a < 0:
        return wrap(a + 360)
    
    if a > 360:
        return wrap(a - 360)

    return a

def read():

    # read two bytes
    l,r = spi.readbytes(2)

    # convert to an integer representing the angle
    s = (((l & 0xFF) << 8) | (r & 0xFF)) & ~0xC000

    # convert integer to angle in degrees
    return (s-8192)/8192 * 360

def calibrate(N=100):
    s = sum(read() for i in range(N))
    return s/N

offset = calibrate()

print("CALIBRATION COMPLETE")
print("STARTING TO PUBLISH")

while True:
    theta = wrap(read() - offset)

    #print(theta)

    msg = angle_t();
    msg.angle = theta;
    lc.publish("ANGLE", msg.encode())
