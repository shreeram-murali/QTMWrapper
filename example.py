import time
from mocapwrapper import QTMWrapper, QTMWrapper6DOF
import numpy as np

IP = '192.168.0.102'
BOUNDS = (-1500, 2500, -1000, 1000, -100, 3000) # xmin, xmax, ymin, ymax, zmin, zmax -- bounding box all values in mm
BODY_NAME = 'cf1'

mocap = QTMWrapper6DOF(IP, BOUNDS, BODY_NAME)
time.sleep(0.1)
s = time.time()
while True:
    p = mocap.getpose()
    print(f'The position is {p.pos} and \n the rotation matrix is {p.rot}')
    time.sleep(0.01)
    if time.time() - s > 5:
        break
mocap.close()  