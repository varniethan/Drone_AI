import time

import numpy as np

from udacidrone import Drone
from udacidrone.connection import MavlinkConnection

conn = MavlinkConnection('tcp:127.0.0.1:5760', threaded=True)
dr = Drone(conn)

time.sleep(0.5)
dr.start()

time.sleep(0.5)
dr.take_control()

time.sleep(0.5)
dr.arm()

time.sleep(0.5)
dr.takeoff(5)

time.sleep(3)

#e
starting_pos = dr.local_position
print(dr.local_position)
time.sleep(0.5)
dr.cmd_position(5,-10, 10, np.pi/2)
time.sleep(10)
dr.cmd_position(starting_pos[0], starting_pos[1], -starting_pos[2], 0)
      
#e
time.sleep(10)
dr.takeoff(1)
time.sleep(1)
dr.land()
time.sleep(0.5)
dr.disarm()
time.sleep(0.5)
dr.release_control()
