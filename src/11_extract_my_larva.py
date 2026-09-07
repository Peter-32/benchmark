import sc2reader
import pandas as pd
import numpy as np
import tqdm
from glob import glob
from utils import *

all_dfs = []
game_number = 0
for account in ['sample']:
    files = glob(f'../data/input/my_data/{account}/*')
    for file in tqdm.tqdm(files):
        
        try:
            replay = sc2reader.load_replay(file, load_map=True, load_level=4)
        except Exception as e:
            print(f"Failed to load {file}: {e}")
            continue
        if replay.map_name in ['Ruby Rock LE', 'Emerald City CE', 'Reclamation LE', 'Fields of Death', 'Gemgarden LE', 'New Bed of Chaos LE', 'Rhoskallian LE', 'Rust Bucket LE', 'Sludge City', 'Undercurrent LE', 'Yellowjacket', 'Phantom Mode']:
            continue
        game_number += 1
        assert replay.map_name in ['valid_maps', "At Eternity's Edge LE", 'Blackrock LE', 'Fear and Faith LE', 'Rainfall LE', 'Sanctuary III LE', 'Lockdown LE', 'Washout LE', 'Rorschach LE', 'Old Sun Temple LE'], replay.map_name

        is_valid_release = replay.release_string >= '5.0.16'
        assert is_valid_release, replay.release_string
        
        player1 = 'nemo'
        player2 = None
        player1_won = None
        player1_race = 'Zerg'
        player2_race = None
        for player in replay.players:
            if player.name == 'nemo' or player.name == 'Kairo':
                assert player.play_race == 'Zerg'
                player1_won = player.result
            else:
                if player2 != None:
                    raise Exception(player.name, player2)
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
local.write.csv(output_df, '11_extract_my_larva')
