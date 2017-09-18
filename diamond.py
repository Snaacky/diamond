import keyboard
import pymem
import pymem.process
import time

from config import *

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_id, "client.dll").base_address

def main():
    print("Diamond has launched. Toggle walls with: {}.".format(toggle_key))
    toggled = False

    while True:
        try:
            if keyboard.is_pressed(toggle_key):
                if not toggled:
                    toggled = True
                    print("Walls has been toggled on.")
                    time.sleep(1)
                else:
                    toggled = False
                    print("Walls has been toggled off.")
                    time.sleep(1)
        except RuntimeError: # Keyboard throws RuntimeError on key press.
            pass

        if toggled:
            try:
                for i in range(0, 32): 
                    glow_player_glow_index = pm.read_int(get_glow_current_player(i) + m_iGlowIndex)
                    entity_team_id = pm.read_int(get_glow_current_player(i) + m_iTeamNum)

                    if entity_team_id is 2: # Terrorist
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x4)), t_red)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x8)), t_green)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0xC)), t_blue)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x10)), t_alpha)
                        pm.write_int((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x24)), 1)

                    if entity_team_id is 3: # Counter-Terrorist
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x4)), ct_red) 
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x8)), ct_green)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0xC)), ct_blue)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x10)), ct_alpha)
                        pm.write_int((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x24)), 1)

            except pymem.exception.MemoryReadError: # Attempted to read invalid entity.
                pass

def get_glow_current_player(index):
    return pm.read_int(client + dwEntityList + index * 0x10)

def get_glow_pointer():
    return pm.read_int(client + dwGlowObjectManager)

if __name__ == '__main__':
    main()