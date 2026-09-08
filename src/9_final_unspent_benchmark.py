from utils import *
import pandas as pd
import matplotlib.pyplot as plt
base_project_folder = get_base_project_folder()


my_df = local.read.csv("8_my_unspent_transform", 'interim')
my_terran_df = my_df.query('opponent_race == "Terran"')
my_terran_aggregated_data = my_terran_df.groupby('second')['unspent_amount'].quantile(0.50)[:-50]
my_terran_aggregated_data

pro_df = local.read.csv("8_pro_unspent_transform", 'interim')
pro_terran_df = pro_df.query('opponent_race == "Terran"')
pro_terran_aggregated_data = pro_terran_df.groupby('second')['unspent_amount'].quantile(0.20)[:-50]
pro_terran_aggregated_data

plt.plot(my_terran_aggregated_data)
plt.plot(pro_terran_aggregated_data)
score = sum(pro_terran_aggregated_data) / sum(my_terran_aggregated_data)
plt.legend(['my cumulative unspent resources', 'pro cumulative unspent resources'])
plt.title(f"Unspent ZvT Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_unspent_zvt_benchmark.png")
plt.clf()

my_zerg_df = my_df.query('opponent_race == "Zerg"')
my_zerg_aggregated_data = my_zerg_df.groupby('second')['unspent_amount'].quantile(0.50)[:-50]
my_zerg_aggregated_data

pro_zerg_df = pro_df.query('opponent_race == "Zerg"')
pro_zerg_aggregated_data = pro_zerg_df.groupby('second')['unspent_amount'].quantile(0.20)[:-50]
pro_zerg_aggregated_data

plt.plot(my_zerg_aggregated_data)
plt.plot(pro_zerg_aggregated_data)
score = sum(pro_zerg_aggregated_data) / sum(my_zerg_aggregated_data)
plt.legend(['my cumulative unspent resources', 'pro cumulative unspent resources'])
plt.title(f"Unspent ZvZ Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_unspent_zvz_benchmark.png")
plt.clf()

my_protoss_df = my_df.query('opponent_race == "Protoss"')
my_protoss_aggregated_data = my_protoss_df.groupby('second')['unspent_amount'].quantile(0.50)[:-50]
my_protoss_aggregated_data

pro_protoss_df = pro_df.query('opponent_race == "Protoss"')
pro_protoss_aggregated_data = pro_protoss_df.groupby('second')['unspent_amount'].quantile(0.20)[:-50]
pro_protoss_aggregated_data

plt.plot(my_protoss_aggregated_data)
plt.plot(pro_protoss_aggregated_data)
score = sum(pro_protoss_aggregated_data) / sum(my_protoss_aggregated_data)
plt.legend(['my cumulative unspent resources', 'pro cumulative unspent resources'])
plt.title(f"Unspent ZvP Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_unspent_zvp_benchmark.png")
plt.clf()
