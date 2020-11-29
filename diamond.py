from pymem import Pymem,process,exception
import requests

try:
    r = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json").json()
    offsets = {"dwEntityList": r['signatures']['dwEntityList'],
               "dwGlowObjectManager": r['signatures']['dwGlowObjectManager'],
               "m_iGlowIndex": r['netvars']['m_iGlowIndex'],
               "m_iTeamNum": r['netvars']['m_iTeamNum']
              }

    processName='csgo.exe'
    pm = Pymem(processName)
    client = process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    print("Diamond has launched.")

    abierto=True
    while abierto:
        glow_manager = pm.read_int(client + offsets['dwGlowObjectManager'])

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + offsets['dwEntityList'] + i * 0x10)

            if entity: 
                entity_team_id = pm.read_int(entity + offsets['m_iTeamNum'])
                entity_glow = pm.read_int(entity + offsets['m_iGlowIndex'])

                gMPEGM38=glow_manager + entity_glow * 0x38

                row=entity_team_id-2
                colores=[[1.0,0.0,0.0,1.0], # Terrorist
                         [0.0,0.0,1.0,1.0]] # Counter-terrorist
                pm.write_float(gMPEGM38 + 0x4, colores[row][0])   # R 
                pm.write_float(gMPEGM38 + 0x8, colores[row][1])   # G
                pm.write_float(gMPEGM38 + 0xC, colores[row][2])   # B
                pm.write_float(gMPEGM38 + 0x10, colores[row][3])  # Alpha

                pm.write_int(gMPEGM38 + 0x24, 1)           # Enable glow

except exception.ProcessNotFound:
    print("error: couldn't find process",processName)

        
        
        
