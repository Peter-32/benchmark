import sc2reader
import pandas as pd
import numpy as np
import tqdm
from glob import glob

all_dfs = []
game_number = 0
for account in ['account1', 'account2', 'account3']:
    files = glob(f'../data/input/my_data/{account}/*')
    for file in tqdm.tqdm(files):
        game_number += 1
        try:
            replay = sc2reader.load_replay(file, load_map=True)
        except Exception as e:
            print(f"Failed to load {file}: {e}")
            continue
        
        assert replay.map_name in ['valid_maps', 'Blackrock LE', 'Fear and Faith LE', 'Rainfall LE', 'Sanctuary III LE', 'Lockdown LE', 'Washout LE', 'Rorschach LE', 'Old Sun Temple LE'], replay.map_name

        is_valid_release = replay.release_string >= '5.0.16'
        assert is_valid_release, replay.release_string
        
        player1 = 'Serral'
        player2 = None
        player1_won = None
        player1_race = 'Zerg'
        player2_race = None
        for player in replay.players:
            if player.name == 'nemo':
                assert player.play_race == 'Zerg'
                player1_won = player.result
            else:
                if player2 != None:
                    raise Exception(player.name, player2)
                player2 = player.name
                player2_race = player.play_race
        print(player1, player2, player1_race, player2_race)

        inject_times_data = []
        for event in replay.events:
            seconds = event.frame / 22.4
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            if seconds < 1:
                continue
        
            try:
                if playername != 'Serral':
                    continue
            except:
                pass
        
            if event.name == 'TargetUnitCommandEvent':
                if event.ability == None:
                    continue
                if event.ability.name == 'SpawnLarva':
                    inject_times_data.append(seconds)
            if seconds > 10*60:
                break
        inject_times_df = pd.DataFrame()
        inject_times_df['inject_time'] = inject_times_data
        inject_times_df['game_number'] = game_number
        inject_times_df['opponent_race'] = player2_race
        inject_times_df['game_length_seconds_max_600'] = int(np.round(seconds,0))
        inject_times_df['main_player_won'] = player1_won
        inject_times_df = inject_times_df[['game_number', 'opponent_race', 'game_length_seconds_max_600', 'inject_time']]
        all_dfs.append(inject_times_df)
inject_times_df = pd.concat(all_dfs, axis='index', ignore_index=True)
local.write.csv(inject_times_df, '2_extract_pro_injects')