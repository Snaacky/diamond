import pymem
import pymem.process
import enum
import keyboard

class Team(enum.Enum):
    UNKNOWN = 0
    TERRORIST = 2
    COUNTER_TERRORIST = 3

dwEntityList = 0x4DA31EC
dwGlowObjectManager = 0x52EB678
m_iGlowIndex = 0xA438
m_iTeamNum = 0xF4


def set_glow(pm, glow_manager, entity_glow, r, g, b, a):
    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(r))
    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(g))
    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(b))
    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(a))
    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

def main():
    print("Diamond has launched.")
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            break  # finishing the script

        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == Team.TERRORIST.value: 
                    set_glow(pm, glow_manager, entity_glow, 1, 0, 0, 1)
                elif entity_team_id == Team.COUNTER_TERRORIST.value:
                    set_glow(pm, glow_manager, entity_glow, 0, 0, 1, 1)

if __name__ == '__main__':
    main()
