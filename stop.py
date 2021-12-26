import asyncio
import moteus
import lcm

lc = lcm.LCM()

lc.publish("STOP", bytes(0))

# async def stop():
#     lc.publish("STOP", bytes(0))

#     # c = moteus.Controller()
#     # await c.set_stop()

# if __name__ == '__main__':
#     asyncio.run( stop() )
    
