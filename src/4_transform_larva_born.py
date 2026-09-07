import pandas as pd
from utils import *
import matplotlib.pyplot as plt

pro_df = local.read.csv('2_extract_pro_larva_borns', 'interim')
pro_df = pro_df.query("game_length_seconds_max_600 >= 420")
my_df = local.read.csv('3_extract_my_larva_borns', 'interim')
my_df = my_df.query("game_length_seconds_max_600 >= 420")
print("shape", pro_df.shape, my_df.shape)

dfs = []
for game_number in pro_df.game_number.unique():
    pro_df_one_game = pro_df.query(f'game_number == {game_number}')
    input_data = list(pro_df_one_game.sort_values(by='larva_born_time')['larva_born_time'].values)

    data_i = []
    cumulative_count = []
    j = 0
    current_cumulative = 0
    i = 0
    for j in range(len(input_data)):
        while i < input_data[j]:
            data_i.append(i)
            cumulative_count.append(current_cumulative)
            i += 1
        current_cumulative += 1

    pro_data_cumulative_df = pd.DataFrame()
    pro_data_cumulative_df['second'] = data_i
    pro_data_cumulative_df['game_number'] = game_number
    pro_data_cumulative_df['larva_born_count'] = cumulative_count
    pro_data_cumulative_df['opponent_race'] = pro_df_one_game.iloc[0]['opponent_race']
    dfs.append(pro_data_cumulative_df)
pro_df_output = pd.concat(dfs, axis='index', ignore_index=True)
local.write.csv(pro_df_output, '4_pro_larva_born_transform')


dfs = []
for game_number in my_df.game_number.unique():
    my_df_one_game = my_df.query(f'game_number == {game_number}')
    input_data = list(my_df_one_game.sort_values(by='larva_born_time')['larva_born_time'].values)

    data_i = []
    cumulative_count = []
    j = 0
    current_cumulative = 0
    i = 0
    for j in range(len(input_data)):
        while i < input_data[j]:
            data_i.append(i)
            cumulative_count.append(current_cumulative)
            i += 1
        current_cumulative += 1

    my_data_cumulative_df = pd.DataFrame()
    my_data_cumulative_df['second'] = data_i
    my_data_cumulative_df['game_number'] = game_number
    my_data_cumulative_df['larva_born_count'] = cumulative_count
    my_data_cumulative_df['opponent_race'] = my_df_one_game.iloc[0]['opponent_race']
    dfs.append(my_data_cumulative_df)
my_df_output = pd.concat(dfs, axis='index', ignore_index=True)
local.write.csv(my_df_output, '4_my_larva_born_transform')
