import pymem
import pymem.process

dwEntityList = (0x4A8473C)
dwGlowObjectManager = (0x4FB14E8)
m_iGlowIndex = (0xA310)
m_iTeamNum = (0xF0)

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_id, "client.dll").base_address

def main():
    print("Diamond has launched.")

    while True:
        if pm.read_int(client + dwEntityList) > 0:
            glow_manager = pm.read_int(client + dwGlowObjectManager)

            for i in range(1, 32): # entities 1-32 are reserved for players. 
                entity = pm.read_int(client + dwEntityList + i * 0x10)

                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_glow = pm.read_int(entity + m_iGlowIndex)

                    if entity_team_id == 2:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))  # R 
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))  # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) # Alpha
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) # Enable glow
                        
                    elif entity_team_id == 3:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))  # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))  # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) # Alpha
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) # Enable glow

if __name__ == '__main__':
    main()