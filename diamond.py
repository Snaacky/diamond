import pymem
import pymem.process

dwEntityList = (0x4A8473C)
dwGlowObjectManager = (0x4FB14E8)
m_iGlowIndex = (0xA310)
m_iTeamNum = (0xF0)

t_red = float(1)
t_green = float(0)
t_blue = float(0)
t_alpha = float(1)
ct_red = float(0)
ct_green = float(0)
ct_blue = float(1)
ct_alpha = float(1)

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_id, "client.dll").base_address

def main():
    print("Diamond has launched.")

    while True:
        # check if player is in-game (if entity list exists)
        if pm.read_int(client + dwEntityList) > 0:
            for i in range(0, 32): 
                glow_manager = pm.read_int(client + dwGlowObjectManager)
                entity = pm.read_int(client + dwEntityList + 0x10 * i)

                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_glow = pm.read_int(entity + m_iGlowIndex)

                    if entity_team_id and int(entity_team_id) == 2:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, t_red)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, t_green)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, t_blue)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, t_alpha)
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
                        
                    elif entity_team_id and int(entity_team_id) == 3:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, ct_red)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, ct_green)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, ct_blue)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, ct_alpha)
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)

if __name__ == '__main__':
    main()