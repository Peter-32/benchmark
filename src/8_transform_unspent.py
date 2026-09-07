import pandas as pd
from utils import *
import matplotlib.pyplot as plt

pro_df = local.read.csv('2_extract_pro_injects', 'interim')
pro_df = pro_df.query("game_length_seconds_max_600 >= 420")
my_df = local.read.csv('3_extract_my_injects', 'interim')
my_df = my_df.query("game_length_seconds_max_600 >= 420")
print("shape", pro_df.shape, my_df.shape)

dfs = []
for game_number in pro_df.game_number.unique():
    pro_df_one_game = pro_df.query(f'game_number == {game_number}')
    print(pro_df_one_game)

    data_i = []
    cumulative_count = []
    for i in range(0, 601):
        data_i.append(i)
        cumulative_count.append(pro_df_one_game.query(f'inject_time < {i}').shape[0])
    pro_data_cumulative_df = pd.DataFrame()
    pro_data_cumulative_df['second'] = data_i
    pro_data_cumulative_df['game_number'] = game_number
    pro_data_cumulative_df['inject_count'] = cumulative_count
    pro_data_cumulative_df['opponent_race'] = pro_df_one_game.iloc[0]['opponent_race']
    dfs.append(pro_data_cumulative_df)
pro_df = pd.concat(dfs, axis='index', ignore_index=True)
local.write.csv(pro_df, '4_pro_inject_transform')


dfs = []
for game_number in my_df.game_number.unique():
    my_df_one_game = my_df.query(f'game_number == {game_number}')
    print(my_df_one_game)

    data_i = []
    cumulative_count = []
    for i in range(0, 601):
        data_i.append(i)
        cumulative_count.append(my_df_one_game.query(f'inject_time < {i}').shape[0])
    my_data_cumulative_df = pd.DataFrame()
    my_data_cumulative_df['second'] = data_i
    my_data_cumulative_df['game_number'] = game_number
    my_data_cumulative_df['inject_count'] = cumulative_count
    my_data_cumulative_df['opponent_race'] = my_df_one_game.iloc[0]['opponent_race']
    dfs.append(my_data_cumulative_df)
my_df = pd.concat(dfs, axis='index', ignore_index=True)
local.write.csv(my_df, '4_my_inject_transform')


# plt.plot(pro_data_cumulative_df.second, pro_data_cumulative_df.inject_count)
# plt.savefig('../data/interim/4_pro_plot.png', dpi=300)
