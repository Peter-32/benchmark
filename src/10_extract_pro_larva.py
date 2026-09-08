import sc2reader
import pandas as pd
import numpy as np
import tqdm
from utils import *
from glob import glob

game_number = 0
base_project_folder = get_base_project_folder()
files = glob(f'{base_project_folder}/data/input/pro_data/*')
all_dfs = []
for file in tqdm.tqdm(files):
    game_number += 1
    try:
        replay = sc2reader.load_replay(file, load_map=True, load_level=4)
    except Exception as e:
        print(f"Failed to load {file}: {e}")
        continue
    
    assert replay.map_name in ['valid_maps', "At Eternity's Edge LE", 'Blackrock LE', 'Fear and Faith LE', 'Rainfall LE', 'Sanctuary III LE', 'Lockdown LE', 'Washout LE', 'Rorschach LE', 'Old Sun Temple LE'], replay.map_name

    is_valid_release = replay.release_string >= '5.0.16'
    assert is_valid_release, replay.release_string
    
    player1 = 'Serral'
    player2 = None
    player1_won = None
    player1_race = 'Zerg'
    player2_race = None
    for player in replay.players:
        if player.name == 'Serral':
            assert player.play_race == 'Zerg'
            player1_won = player.result
        else:
            player2 = player.name
            player2_race = player.play_race
    print(player1, player2, player1_race, player2_race)
    
    larva_amounts_data = []
    larva_data = []
    current_larva_count = 0
    for event in replay.tracker_events:
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
        
        if "changed to Egg" in str(event):
            current_larva_count = max(0, current_larva_count - 1)
        if "Unit born Larva" in str(event):
            current_larva_count += 1            
            larva_data.append(seconds)
            larva_amounts_data.append(current_larva_count)
        if seconds > 60*10:
            break
    output_df = pd.DataFrame()
    output_df['larva_time'] = larva_data
    output_df['larva_amount'] = larva_amounts_data
    output_df['game_number'] = game_number
    output_df['opponent_race'] = player2_race
    output_df['game_length_seconds_max_600'] = int(np.round(seconds,0))
    output_df['main_player_won'] = player1_won
    output_df = output_df[['game_number', 'opponent_race', 'game_length_seconds_max_600', 'larva_time', 'larva_amount']]
    all_dfs.append(output_df)
output_df = pd.concat(all_dfs, axis='index', ignore_index=True)
local.write.csv(output_df, '10_extract_pro_larva')
