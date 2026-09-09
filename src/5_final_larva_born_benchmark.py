from utils import *
import pandas as pd
import matplotlib.pyplot as plt
base_project_folder = get_base_project_folder()
   
my_df = local.read.csv("4_my_larva_born_transform", 'interim')
my_terran_df = my_df.query('opponent_race == "Terran"')
my_terran_aggregated_data = my_terran_df.groupby('second')['larva_born_count'].quantile(0.50)[:-50]
my_terran_aggregated_data

pro_df = local.read.csv("4_pro_larva_born_transform", 'interim')
pro_terran_df = pro_df.query('opponent_race == "Terran"')
pro_terran_aggregated_data = pro_terran_df.groupby('second')['larva_born_count'].quantile(0.80)[:-50]
print(",".join(list([str(x) for x in pro_terran_aggregated_data.values])))

plt.plot(my_terran_aggregated_data)
plt.plot(pro_terran_aggregated_data)
score = sum(my_terran_aggregated_data) / sum(pro_terran_aggregated_data)
plt.legend(['my larva_borns', 'pro larva_borns'])
plt.title(f"larva_born ZvT Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_larva_born_zvt_benchmark.png")
plt.clf()

my_zerg_df = my_df.query('opponent_race == "Zerg"')
my_zerg_aggregated_data = my_zerg_df.groupby('second')['larva_born_count'].quantile(0.50)[:-50]
my_zerg_aggregated_data

pro_zerg_df = pro_df.query('opponent_race == "Zerg"')
pro_zerg_aggregated_data = pro_zerg_df.groupby('second')['larva_born_count'].quantile(0.80)[:-50]
print(",".join(list([str(x) for x in pro_zerg_aggregated_data.values])))

plt.plot(my_zerg_aggregated_data)
plt.plot(pro_zerg_aggregated_data)
score = sum(my_zerg_aggregated_data) / sum(pro_zerg_aggregated_data)

plt.legend(['my larva_borns', 'pro larva_borns'])
plt.title(f"larva_born ZvZ Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_larva_born_zvz_benchmark.png")
plt.clf()

my_protoss_df = my_df.query('opponent_race == "Protoss"')
my_protoss_aggregated_data = my_protoss_df.groupby('second')['larva_born_count'].quantile(0.50)[:-50]
my_protoss_aggregated_data

pro_protoss_df = pro_df.query('opponent_race == "Protoss"')
pro_protoss_aggregated_data = pro_protoss_df.groupby('second')['larva_born_count'].quantile(0.80)[:-50]
print(",".join(list([str(x) for x in pro_protoss_aggregated_data.values])))

plt.plot(my_protoss_aggregated_data)
plt.plot(pro_protoss_aggregated_data)
score = sum(my_protoss_aggregated_data) / sum(pro_protoss_aggregated_data)

plt.legend(['my larva_borns', 'pro larva_borns'])
plt.title(f"larva_born ZvP Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_larva_born_zvp_benchmark.png")
plt.clf()
