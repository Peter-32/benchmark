import sc2reader
import pandas as pd
import numpy as np
import tqdm
from glob import glob
from utils import *

all_dfs = []
game_number = 0
for account in ['sample']:
    base_project_folder = get_base_project_folder()
    files = glob(f'{base_project_folder}/data/input/my_data/{account}/*')
    for file in tqdm.tqdm(files):
        
        try:
            replay = sc2reader.load_replay(file, load_map=True)
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

        larva_born_times_data = []
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
            if event.name == "UnitBornEvent" and event.unit_type_name == "Larva":
                larva_born_times_data.append(seconds)
            if seconds > 10*60:
                break
        larva_born_times_df = pd.DataFrame()
        larva_born_times_df['larva_born_time'] = larva_born_times_data
        larva_born_times_df['game_number'] = game_number
        larva_born_times_df['opponent_race'] = player2_race
        larva_born_times_df['game_length_seconds_max_600'] = int(np.round(seconds,0))
        larva_born_times_df['main_player_won'] = player1_won
        larva_born_times_df = larva_born_times_df[['game_number', 'opponent_race', 'game_length_seconds_max_600', 'larva_born_time', 'main_player_won']]
        all_dfs.append(larva_born_times_df)
larva_born_times_df = pd.concat(all_dfs, axis='index', ignore_index=True)
local.write.csv(larva_born_times_df, '3_extract_my_larva_borns')