import asyncio
from threading import Thread
import numpy as np
import qtm

class QTMWrapper(Thread):
    """Run QTM Wrapper on its own thread."""
    def __init__(self, qtm_ip, bounds):
        Thread.__init__(self)

        # self.body_name = body_name
        self.on_pose = None
        self.connection = None
        self._stay_open = True
        self.qtm_ip = qtm_ip
        self._bounds = bounds
        self._markers = None

        self._previous_frame = 0 
        self._previous_height = 0.1

        self.start()
    
    def close(self):
        self._stay_open = False
        self.join()
    
    def run(self):
        asyncio.run(self._life_cycle())
    
    async def _life_cycle(self):
        await self._connect()
        while self._stay_open:
            await asyncio.sleep(1)
        await self._close()

    async def _connect(self):
        host = self.qtm_ip
        print('Connecting to QTM on ' + host)
        self.connection = await qtm.connect(host)

        await self.connection.stream_frames(components=['3d'], on_packet=self._on_packet)
        # await asyncio.sleep(10)
        # await self.connection.stream_frames_stop()
    
    def _on_packet(self, packet):
        header, self._markers = packet.get_3d_markers()
        pos = {'x':[], 'y':[], 'z':[]}
        for i in self._markers:
            pos['x'].append(i.x)
            pos['y'].append(i.y)
            pos['z'].append(i.z)
        self.x = np.average(np.array(pos['x']))
        self.y = np.average(np.array(pos['y']))
        self.z = np.average(np.array(pos['z']))
    
    def getpose(self):
        return (self.x, self.y, self.z)

    def geofence_check(self):
        try:
            for i in self._markers:
                    if i.x < self._bounds[0] or i.x > self._bounds[1] or i.y < self._bounds[2] or i.y > self._bounds[3] or i.z < self._bounds[4] or i.z > self._bounds[5]:
                        print("Object outside of bounding limits.")
                        return False
                    else:
                        return True
        except TypeError:
            pass

    def help(self):
        print("The required modules can be imported with: \n")
        print("1. import asyncio \n2. from threading import Thread")
        print("3. import numpy as np \n4. import qtm")
        self.close()

    async def _close(self):
        await self.connection.stream_frames_stop()
        self.connection.disconnect()