import pymem
import pymem.process
import requests

def retrieve_offsets():
    r = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json").json()
    offsets = {
        "dwEntityList": r['signatures']['dwEntityList'],
        "dwGlowObjectManager": r['signatures']['dwGlowObjectManager'],
        "m_iGlowIndex": r['netvars']['m_iGlowIndex'],
        "m_iTeamNum": r['netvars']['m_iTeamNum']
    }
    return offsets


def main(offsets):
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        glow_manager = pm.read_int(client + offsets['dwGlowObjectManager'])

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + offsets['dwEntityList'] + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + offsets['m_iTeamNum'])
                entity_glow = pm.read_int(entity + offsets['m_iGlowIndex'])

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R 
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow


if __name__ == '__main__':
    print("Diamond has launched.")
    required_offsets = retrieve_offsets()
    main(required_offsets)
