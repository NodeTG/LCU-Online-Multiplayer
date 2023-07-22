import asyncio
import pickle
import copy

from websockets.server import serve


class Player():
    def __init__(self, pid: int = 0, pos: list = [0,1000,0], rot: int = 0, disguise: int = 1, anim: int = 0, vehicle: int = 0, connected: bool = False):
        self.pid = pid
        self.pos = pos
        self.rot = rot
        self.disguise = disguise
        self.anim = anim
        self.vehicle = vehicle
        self.connected = connected


#class ServerState():
#    def __init__(self):
#        self.players = [Player(0),
#                        Player(1),
#                        Player(2),
#                        Player(3)]


class QueueItem():
    def __init__(self, player: Player, cmd: int = 0, sys_data: int = 0):
        self.cmd = cmd
        self.player = player
        self.sys_data = sys_data


clients = {
    0: None,
    1: None,
    2: None,
    3: None,
    4: None,
    5: None
}


queue = [
    [],
    [],
    [],
    [],
    [],
    []
]


async def handle_disconnect(pid: int):
    clients[pid] = None
    print(f"DISCONNECTION: {pid}")
    #print(f"queue len: {len(queue[0])}")


async def on_connect(ws):
    pid = -1
    for i in range(6):
        if clients[i] is None:
            clients[i] = ws
            pid = i
            break
    
    if pid == -1:
        return
    
    await ws.send(str(pid))
    print(f"NEW CLIENT: {pid}")

    #queue[pid] = []

    while True:
        try:
            data = await ws.recv()
            data = pickle.loads(data)

            for i in range(6):
                if i == pid:
                    continue

                dupe = None
                for item in queue[i]:
                    if item.cmd == data.cmd:
                        dupe = item
                        break
                
                if dupe is None:
                    queue[i].append(data)
                else:
                    dupe.player = copy.deepcopy(data.player)
                    dupe_copy = copy.deepcopy(dupe)
                    queue[i].remove(dupe)
                    queue[i].append(dupe_copy)


            if len(queue[pid]) > 0:
                await ws.send(pickle.dumps(queue[pid].pop(0)))
            else:
                await ws.send(pickle.dumps(QueueItem(Player(-1), -1)))
        except Exception as e:
            print(e)
            await handle_disconnect(pid)
            return


async def main():
    async with serve(on_connect, "", 8765):
        await asyncio.Future() 


asyncio.run(main())
