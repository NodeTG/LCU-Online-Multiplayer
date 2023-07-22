import pymeow


def read_offsets(proc, base_address, offsets):
    basepoint = pymeow.read_int64(proc, base_address)

    current_pointer = basepoint

    for i in offsets[:-1]:
        current_pointer = pymeow.read_int64(proc, current_pointer+i)
    
    return current_pointer + offsets[-1]


def reload_addrs():
    global proc, pos_base_addr, rot_base_addr, x_addr, z_addr, y_addr, rot_addr, city_addr
    global act4_mission_addr, act4_stage_addr, act3_mission_addr, act3_stage_addr
    global disguise_class_addr, animation_addr, shuttle_sb_addr, crashmat_sb_addr

    try:
        proc = pymeow.process_by_name("LEGOLCUR_DX11.exe")
    except Exception as e:
        print(f"Failed to get process handle; {e}")
        return

    pos_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x01C77C78
    rot_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x01C74920
    city_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x17F86A0
    a4m_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x017ECA08
    a4s_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x017ECA08
    a3m_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x01802620
    a3s_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x01802620
    disguise_class_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x183D070
    animation_base_addr = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x01C74920


    x_addr = read_offsets(proc, pos_base_addr, [0x90])
    y_addr = read_offsets(proc, pos_base_addr, [0x94])
    z_addr = read_offsets(proc, pos_base_addr, [0x98])
    rot_addr = read_offsets(proc, rot_base_addr, [0x218])
    act4_mission_addr = read_offsets(proc, a4m_base_addr, [0x48, 0x60, 0x68, 0x38, 0x88])
    act4_stage_addr = read_offsets(proc, a4s_base_addr, [0x48, 0x60, 0x68, 0x38, 0x60])
    act3_mission_addr = read_offsets(proc, a3m_base_addr, [0x10])
    act3_stage_addr = read_offsets(proc, a3s_base_addr, [0x30, 0x10])
    animation_addr = read_offsets(proc, animation_base_addr, [0x7A0])
    shuttle_sb_addr = read_offsets(proc, a3s_base_addr, [0x30, -0x53F8])    # THIS IS CURSED, THERE'S NO WAY IT WILL KEEP WORKING
    crashmat_sb_addr = read_offsets(proc, a3s_base_addr, [0x30, -0x4F28])    # THIS IS ALSO CURSED


def read_positions():
    return [pymeow.read_float(proc, x_addr), pymeow.read_float(proc, y_addr), pymeow.read_float(proc, z_addr)]


def read_rotation():
    return pymeow.read_int(proc, shuttle_sb_addr) - (read_vehicle() * 1000)


def read_rotation_old():
    return pymeow.read_float(proc, rot_addr)


def check_city_loaded():
    return pymeow.read_int(proc, city_addr)


def get_disguise_class():
    disguise_class = pymeow.read_int(proc, disguise_class_addr)
    disguise_class += 1
    if disguise_class >= 8:
        disguise_class = 0
    return disguise_class


def read_vehicle():
    return pymeow.read_int(proc, shuttle_sb_addr) // 1000


def read_animation():
    return pymeow.read_int(proc, animation_addr)


def read_act_data():
    return [pymeow.read_int(proc, act4_mission_addr),
            pymeow.read_int(proc, act4_stage_addr),
            pymeow.read_int(proc, act3_mission_addr),
            pymeow.read_int(proc, act3_stage_addr)]


def write_act_data(x: int, y: int, z: int, c: int):
    pymeow.write_int(proc, act4_mission_addr, x)
    pymeow.write_int(proc, act4_stage_addr, y)
    pymeow.write_int(proc, act3_mission_addr, z)
    pymeow.write_int(proc, act3_stage_addr, c)


def write_sb_data(data: int):
    pymeow.write_int(proc, crashmat_sb_addr, data)



try:
    proc = pymeow.process_by_name("LEGOLCUR_DX11.exe")
    reload_addrs()
except Exception as e:
    input(f"Failed to get process handle; {e}\nMake sure that LCU is running!")
    exit()
