import asyncio
import numpy as np
import moteus
import time

import lcm
from moteus_lcm import motor_state_t, command_t;



class Interface:

    def __init__(self, motor_id=1):

        # CREATE LCM COMMUNICATION
        self.lc = lcm.LCM()
        self.subs_cmd = self.lc.subscribe("COMMAND", self.command_handler)
        self.subs_stop = self.lc.subscribe("STOP", self.stop_handler)


        # START MOTEUS CONTROLLER
        self.c = moteus.Controller()

        self.started = False
        self.stopped = False

    def command_handler(self, channel, data):
        msg = command_t.decode(data)
        print("Received Command!")
        self.cmd_pos = msg.pos
        #self.cmd_stop_pos = msg.stop_pos
        #self.cmd_vel = msg.vel
        #self.cmd_max_torque = msg.max_torque

    def stop_handler(self, channel, data):
        self.stopped = True
        #self.stop()
        print("STOP COMMAND RECEIVED FROM LCM")
        #self.stopped = True
        

    async def match_target(self):
        
        if self.stopped:
            await self.c.set_stop()
            return
    
        if not self.started:
            self.state = await self.c.set_stop(query = True)
            self.cmd_pos = self.state.values[moteus.Register.POSITION];
            self.last_pos = self.cmd_pos
            print(f"Grabbed Desired Pos {self.cmd_pos:.3f}")
            self.started = True
            return
        
        print(f"LAST POS: {self.last_pos: 3.3f} CMD POS: {self.cmd_pos: 3.3f}")

        self.state = await self.c.set_position(position = None,#np.nan,
                                          velocity = -5.0 * (self.last_pos - self.cmd_pos), #self.cmd_vel,
                                          maximum_torque=2.0,#self.cmd_max_torque,
                                          query = True,
                                          kp_scale= 0.0)
        self.last_pos = self.state.values[moteus.Register.POSITION];

    def publish_state(self):
        
        #state = await self.c.query()
       
        if not self.started: return
        
        # construct the message
        state = self.state

        msg = motor_state_t()
        msg.mode          = state.values[moteus.Register.MODE]
        msg.position      = state.values[moteus.Register.POSITION]
        msg.velocity      = state.values[moteus.Register.VELOCITY]
        msg.torque        = state.values[moteus.Register.TORQUE]
        #msg.q_current    = state.values[moteus.Register.Q_CURRENT]
        #msg.d_current    = state.values[moteus.Register.D_CURRENT]
        #msg.abs_position = state.values[moteus.Register.ABS_POSITION]
        #msg.rezero_state = state.values[moteus.Register.REZERO_STATE]
        msg.voltage       = state.values[moteus.Register.VOLTAGE]
        msg.temperature   = state.values[moteus.Register.TEMPERATURE]
        msg.fault         = state.values[moteus.Register.FAULT]

        self.lc.publish("MOTOR_STATE", msg.encode())
         
        #print("mode: ", state.values[moteus.Register.MODE],
        #    "pos: ", state.values[moteus.Register.POSITION],
        #    "target: ", self.target_pos)

    async def run(self):

        while True:
            self.lc.handle_timeout(1)
            await self.match_target()
            self.publish_state()

        #last_start = time.time_ns()
        #rate = 20_000_000 # 20 ns

        # try:
        #while not self.stopped:
            # print(time.time_ns() - last_start)
            #last_start = time.time_ns()
            #await self.publish_state()
            #await self.match_target()
            #self.lc.handle_timeout(1)
            # await asyncio.sleep(0.05) # in seconds
            #await asyncio.sleep(1e-9 * (rate - (time.time_ns() - last_start)))
        # except KeyboardInterrupt:
        #     await self.c.set_stop()
        #     raise

    #async def stop(self):

        # print("STOP COMMANDED")
        # self.stopped = True
        #await self.c.set_stop()


if __name__ == '__main__':
    interface = Interface()

    asyncio.run(interface.run())


    #loop = asyncio.get_event_loop()
    # try:
    #loop.run_until_complete(interface.run())
    # except:
        # tasks = asyncio.all_tasks()
        # for t in [t for t in tasks if not (t.done() or t.cancelled())]:
        #     # give canceled tasks the last chance to run
        #     loop.run_until_complete(t)
    # asyncio.run(interface.stop())

    # main_task = asyncio.create_task(interface.run)
    # try:
    #     asyncio.gather(main_task)
    # except KeyboardInterrupt:
    #     main_task.cancel()
    #     interface.stop()
    # finally:
    #     asyncio.wait(interface.c.set_stop())

    

