import sc2reader
import pandas as pd
import numpy as np
import tqdm
from utils import *
from glob import glob

game_number = 0
files = glob('../data/input/pro_data/*')
all_dfs = []
for file in tqdm.tqdm(files):
    game_number += 1
    try:
        replay = sc2reader.load_replay(file, load_map=True)
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
    
    supply_amounts_data = []
    supply_data = []
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
        
    
        if event.name == 'PlayerStatsEvent':
            supply_data.append(seconds)
            supply_amounts_data.append(event.food_made - event.food_used)
        if seconds > 10*60:
            break
    output_df = pd.DataFrame()
    output_df['supply_time'] = supply_data
    output_df['supply_amount'] = supply_amounts_data
    output_df['game_number'] = game_number
    output_df['opponent_race'] = player2_race
    output_df['game_length_seconds_max_600'] = int(np.round(seconds,0))
    output_df['main_player_won'] = player1_won
    output_df = output_df[['game_number', 'opponent_race', 'game_length_seconds_max_600', 'supply_time', 'supply_amount']]
    all_dfs.append(output_df)
output_df = pd.concat(all_dfs, axis='index', ignore_index=True)
local.write.csv(output_df, '19_extract_pro_supply')