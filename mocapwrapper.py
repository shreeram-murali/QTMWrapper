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

import asyncio
from threading import Thread
import xml.etree.ElementTree as ET
import pkg_resources
import numpy as np
import qtm

class Pose():
    def __init__(self, pos, rot) -> None:
        self.pos = pos
        self.rot = rot

class QTMWrapper6DOF(Thread):
    """Run QTM Wrapper on its own thread."""
    def __init__(self, qtm_ip, bounds, body_name):
        Thread.__init__(self)

        # self.body_name = body_name
        self.on_pose = None
        self.connection = None
        self._stay_open = True
        self.qtm_ip = qtm_ip
        self._bounds = bounds
        self._markers = None
        self._wanted_body = body_name

        self._previous_frame = 0 
        self._previous_height = 0.1

        self.start()
   
    def _create_body_index(self, xml_string):
        xml = ET.fromstring(xml_string)
        body_to_index = {}
        for i, b in enumerate(xml.findall('*/Body/Name')):
            body_to_index[b.text.strip()] = i
        return body_to_index
   
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
        self._xml_string = await self.connection.get_parameters(['6d'])
        self._body_index = self._create_body_index(self._xml_string)

        await self.connection.stream_frames(components=['6d'], on_packet=self._on_packet)
   
    def _on_packet(self, packet):
        header, bodies = packet.get_6d()
        if self._wanted_body is not None and self._wanted_body in self._body_index:
            wanted_index = self._body_index[self._wanted_body]
            self.pos, self.rot = bodies[wanted_index]
   
    def getpose(self):
        pos = (self.pos.x, self.pos.y, self.pos.z)
        rot = np.array(self.rot.matrix)
        rot = np.reshape(rot, (3, 3))
        pose = Pose(pos, rot)
        return pose

    def geofence_check(self):
        try:
            if self.pos.x < self._bounds[0] or self.pos.x > self._bounds[1] or self.pos.y < self._bounds[2] or self.pos.y > self._bounds[3] or self.pos.z < self._bounds[4] or self.pos.z > self._bounds[5]:
                return False
            else:
                return True
        except TypeError:
            return True

    def help(self):
        print("The required modules can be imported with: \n")
        print("1. import asyncio \n2. from threading import Thread")
        print("3. import numpy as np \n4. import qtm")
        self.close()

    async def _close(self):
        await self.connection.stream_frames_stop()
        self.connection.disconnect()


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
