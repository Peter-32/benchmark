import pandas as pd
from utils import *
import matplotlib.pyplot as plt

pro_df = local.read.csv('10_extract_pro_larva', 'interim')
pro_df = pro_df.query("game_length_seconds_max_600 >= 420")
my_df = local.read.csv('11_extract_my_larva', 'interim')
my_df = my_df.query("game_length_seconds_max_600 >= 420")
print("shape", pro_df.shape, my_df.shape)

dfs = []
for game_number in pro_df.game_number.unique():
    pro_df_one_game = pro_df.query(f'game_number == {game_number}')
    input_data1 = list(pro_df_one_game.sort_values(by='larva_time')['larva_time'].values)
    input_data2 = list(pro_df_one_game.sort_values(by='larva_time')['larva_amount'].values)

    data_i = []
    cumulative_total = []
    j = 0
    current_cumulative = 0
    i = 0
    for j in range(len(input_data1)):
        while i < input_data1[j]:
            data_i.append(i)
            cumulative_total.append(current_cumulative)
            i += 1
        current_cumulative += input_data2[j]

    pro_data_cumulative_df = pd.DataFrame()
    pro_data_cumulative_df['second'] = data_i
    pro_data_cumulative_df['game_number'] = game_number
    pro_data_cumulative_df['larva_amount'] = cumulative_total
    pro_data_cumulative_df['opponent_race'] = pro_df_one_game.iloc[0]['opponent_race']
    dfs.append(pro_data_cumulative_df)
pro_df = pd.concat(dfs, axis='index', ignore_index=True)
local.write.csv(pro_df, '12_pro_larva_transform')


dfs = []
for game_number in my_df.game_number.unique():
    my_df_one_game = my_df.query(f'game_number == {game_number}')
    input_data1 = list(my_df_one_game.sort_values(by='larva_time')['larva_time'].values)
    input_data2 = list(my_df_one_game.sort_values(by='larva_time')['larva_amount'].values)

    data_i = []
    cumulative_total = []
    j = 0
    current_cumulative = 0
    i = 0
    for j in range(len(input_data1)):
        while i < input_data1[j]:
            data_i.append(i)
            cumulative_total.append(current_cumulative)
            i += 1
        current_cumulative += input_data2[j]

    my_data_cumulative_df = pd.DataFrame()
    my_data_cumulative_df['second'] = data_i
    my_data_cumulative_df['game_number'] = game_number
    my_data_cumulative_df['larva_amount'] = cumulative_total
    my_data_cumulative_df['opponent_race'] = my_df_one_game.iloc[0]['opponent_race']
    dfs.append(my_data_cumulative_df)
my_df = pd.concat(dfs, axis='index', ignore_index=True)
local.write.csv(my_df, '12_my_larva_transform')
