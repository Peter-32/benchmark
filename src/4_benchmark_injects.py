import pandas as pd
from utils import *
import matplotlib.pyplot as plt
pro_df = local.read.csv('2_extract_pro_injects', 'interim')

# We will skip very short games for benchmarking analysis 
pro_df = pro_df.query("game_length_seconds_max_600 >= 420")

print(pro_df.groupby('game_length_seconds_max_600').game_number.nunique())

print(pro_df.groupby('opponent_race').game_number.nunique())

print(pro_df)

# Check just one game first
pro_df_one_game = pro_df.query('game_number == 1')
print(pro_df_one_game)

data_i = []
cumulative_count = []
for i in range(0, 601):
    data_i.append(i)
    cumulative_count.append(pro_df_one_game.query(f'inject_time < {i}').shape[0])
pro_data_cumulative_df = pd.DataFrame()
pro_data_cumulative_df['second'] = data_i
pro_data_cumulative_df['inject_count'] = cumulative_count
print(pro_data_cumulative_df)

# # Check the plots of all 3 oponent_race separately and combined first
# terran_benchmarks
# for game_number in pro_df.game_number.unique():

plt.plot(pro_data_cumulative_df)