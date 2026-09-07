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

        creep_times_data = []
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
        
            if 'Unit initiated CreepTumorBurrowed' in str(event) or 'BuildCreepTumor' in str(event):
                creep_times_data.append(seconds)
            if seconds > 10*60:
                break
        creep_times_df = pd.DataFrame()
        creep_times_df['creep_time'] = creep_times_data
        creep_times_df['game_number'] = game_number
        creep_times_df['opponent_race'] = player2_race
        creep_times_df['game_length_seconds_max_600'] = int(np.round(seconds,0))
        creep_times_df['main_player_won'] = player1_won
        creep_times_df = creep_times_df[['game_number', 'opponent_race', 'game_length_seconds_max_600', 'creep_time', 'main_player_won']]
        all_dfs.append(creep_times_df)
creep_times_df = pd.concat(all_dfs, axis='index', ignore_index=True)
local.write.csv(creep_times_df, '16_extract_my_creeps')