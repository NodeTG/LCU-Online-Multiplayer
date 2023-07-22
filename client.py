import random
import math
import pickle
import time
import copy

from mem_stuff import *
from websockets.sync.client import connect


ANIM_DICT = {
    1: 0,       # idle
    5: 3,       # tiptoe
    0: 4,       # walk
    3: 5,       # run
    4: 6,       # sprint
    11: 22,     # idle(1?)
    21: 23,     # idle(2?)
    26: 24,     # idle(3?)
    9: 21,      # jump
    10: 9,      # land
    115: 8,     # fallland
    8: 2,       # fall
    268: 15,    # combatroll_jump (TODO: fix this)
    270: 7,     # combatroll_land (TODO: fix this)
    193: 10,    # wade
    331: 11,    # swim (TODO: fix this)
    327: 12,    # teeter
    432: 17,    # jump_trampoline (TODO: make this loop properly)
    1393: 20,   # shrug
    2916: 26,   # DisguiseBooth_in
    2917: 25,   # DisguiseBooth_idle
    2918: 27,   # DisguiseBooth_out
    45: 28,     # hover
    46: 29,     # fly
    2411: 16,   # ride_car
    2157: 16,   # ride_car (helicopter)
    2407: 16,   # ride_car (motorbike)
    2303: 13,   # Whistle_Run
    2302: 14,   # Whistle
    2133: 30,   # DRC_Intro2
    2134: 31,   # DRC_Outro2
    2135: 32,   # DRC_Idle2
}


class Player():
    def __init__(self, pid: int = 0, pos: list = [0,1000,0], rot: int = 0, disguise: int = 1, anim: int = 0, vehicle: int = 0, connected: bool = False):
        self.pid = pid
        self.pos = pos
        self.rot = rot
        self.disguise = disguise
        self.anim = anim
        self.vehicle = vehicle
        self.connected = connected


class QueueItem():
    def __init__(self, player: Player, cmd: int = 0, sys_data: int = 0):
        self.cmd = cmd
        self.player = player
        self.sys_data = sys_data


pid = -1
local_player = Player(-1)

queue = []

addrs_ready = True
with connect("ws://12.34.56.78:8765") as websocket:
    pid = int(websocket.recv())
    local_player = Player(pid, connected=True)

    print(f"Connected - PID: {pid}")

    while True:
        original = copy.deepcopy(local_player)

        if check_city_loaded() == 0:
            addrs_ready = False
            websocket.send(pickle.dumps(QueueItem(local_player, 0)))
            item = pickle.loads(websocket.recv())
            time.sleep(0.033)
        else:
            if not addrs_ready:
                time.sleep(1)
                reload_addrs()
                addrs_ready = True

            local_player.pos = read_positions()
            #local_player.rot = (read_rotation_old() + math.radians(180)) / 0.00009587380104
            local_player.rot = read_rotation()
            local_player.anim = ANIM_DICT.get(read_animation(), 1)
            local_player.disguise = get_disguise_class()

            vehicle = read_vehicle()
            if vehicle < 0:
                vehicle = 0
            local_player.vehicle = vehicle

            orig_len = len(queue)
            if original.anim != local_player.anim:
                queue.append(QueueItem(local_player, 1))
            if original.disguise != local_player.disguise:
                queue.append(QueueItem(local_player, 2))
            if original.vehicle != local_player.vehicle:
                queue.append(QueueItem(local_player, 3))
            
            if len(queue) == orig_len:
                queue.append(QueueItem(local_player, 0))

            to_remove = []
            ids_in_queue = []
            for i in range(len(queue)-1, -1, -1):
                if queue[i].cmd not in ids_in_queue:
                    ids_in_queue.append(queue[i].cmd)
                else:
                    to_remove.append(queue[i])
            
            while len(to_remove) > 0:
                queue.remove(to_remove.pop())
            
            
            websocket.send(pickle.dumps(queue.pop(0)))
            item = pickle.loads(websocket.recv())

            if item.cmd != -1:
                while not (read_act_data()[3] == 1001):
                    pass

                temp_pos = item.player.pos
                temp_pos[1] -= 0.21
                #temp_rot = int(((item.player.rot + 32768) / 65535) * 360)
                temp_rot = item.player.rot
                temp_pid = item.player.pid
                temp_cmd = item.cmd
                temp_cmd_data = 0

                match temp_cmd:
                    case 0:
                        temp_cmd_data = temp_rot
                    case 1:
                        temp_cmd_data = item.player.anim
                    case 2:
                        temp_cmd_data = item.player.disguise
                    case 3:
                        temp_cmd_data = item.player.vehicle
                    case 4:
                        temp_cmd_data = item.sys_data
                    case _:
                        raise Exception(f"Unknown QueueType: {temp_cmd}")
                
                transmission = str(temp_pid).zfill(1) + str(temp_cmd).zfill(1) + str(temp_cmd_data).zfill(3)

                if len(transmission) > 5:
                    print(f"transmission too long; cannot continue\n{transmission}")
                    exit()
                else:
                    write_act_data(int((temp_pos[0]+2000)*1000), int((temp_pos[1]+2000)*1000), int((temp_pos[2]+2000)*1000), int(transmission))
            
            time.sleep(0.033)
