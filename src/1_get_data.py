import sc2reader
import pandas as pd
import numpy as np
import tqdm
import sys
from utils import *
from glob import glob

path = os.path.join(sys.argv[1], '*')
player_name = sys.argv[2]
files = sorted(glob(path), key=os.path.getmtime, reverse=True)
files_chosen = []
found_zvz = False
found_zvp = False
found_zvt = False
print(files, glob(path), path)
for file in tqdm.tqdm(files):
    try:
        replay = sc2reader.load_replay(file, load_map=True)
    except Exception as e:
        print(f"Failed to load {file}: {e}")
        continue
    
    if not replay.map_name in ["At Eternity's Edge LE", 'Blackrock LE', 'Fear and Faith LE', 'Rainfall LE', 'Sanctuary III LE', 'Lockdown LE', 'Washout LE', 'Rorschach LE', 'Old Sun Temple LE']:
        continue

    if not replay.release_string >= '5.0.16':
        continue
    
    player1 = player_name
    player2 = None
    player1_won = None
    player1_race = None
    player2_race = None
    for player in replay.players:
        if player.name == player_name or player.name == 'Kairo':
            player1_race = player.play_race
            player1_won = player.result
        else:
            if player2 != None:
                raise Exception(player.name, player2)
            player2 = player.name
            player2_race = player.play_race
    # print(player1, player2, player1_race, player2_race)
    if player1_race != 'Zerg':
        continue
    
    for event in replay.events:
        seconds = event.frame / 22.4
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        if seconds < 1:
            continue
    
        try: 
            if player2 in str(event):
                continue           
            if event.player == player2:
                continue
        except:
            pass

        if seconds > 10*60:
            break
    if seconds > 7*60:
        if player2_race == 'Terran' and found_zvt == False:
            files_chosen.append(file)
        if player2_race == 'Zerg' and found_zvz == False:
            files_chosen.append(file)
        if player2_race == 'Protoss' and found_zvp == False:
            files_chosen.append(file)
    if len(files_chosen) >= 3:
        break
print("replays found", len(files_chosen))
if len(files_chosen) < 3:
    raise Exception("Could not found one replay per matchup with 7+ minutes")
folder_path = '../data/input/my_data/sample'
try:
    shutil.rmtree(folder_path)
    print(folder_path)
    os.mkdir(folder_path)
except:
    pass
for file in files_chosen:
    shutil.copy(file, folder_path)
