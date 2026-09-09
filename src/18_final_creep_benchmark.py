from utils import *
import pandas as pd
import matplotlib.pyplot as plt
base_project_folder = get_base_project_folder()

my_df = local.read.csv("17_my_creep_transform", 'interim')
my_terran_df = my_df.query('opponent_race == "Terran"')
my_terran_aggregated_data = my_terran_df.groupby('second')['creep_count'].quantile(0.50)[:-50]
my_terran_aggregated_data

pro_df = local.read.csv("17_pro_creep_transform", 'interim')
pro_terran_df = pro_df.query('opponent_race == "Terran"')
pro_terran_aggregated_data = pro_terran_df.groupby('second')['creep_count'].quantile(0.80)[:-50]
print(",".join(list([str(x) for x in pro_terran_aggregated_data.values])))

plt.plot(my_terran_aggregated_data)
plt.plot(pro_terran_aggregated_data)
score = sum(my_terran_aggregated_data) / sum(pro_terran_aggregated_data)
plt.legend(['my creep', 'pro creep'])
plt.title(f"creep ZvT Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_creep_zvt_benchmark.png")
plt.clf()

my_zerg_df = my_df.query('opponent_race == "Zerg"')
my_zerg_aggregated_data = my_zerg_df.groupby('second')['creep_count'].quantile(0.50)[:-50]
my_zerg_aggregated_data

pro_zerg_df = pro_df.query('opponent_race == "Zerg"')
pro_zerg_aggregated_data = pro_zerg_df.groupby('second')['creep_count'].quantile(0.80)[:-50]
print(",".join(list([str(x) for x in pro_zerg_aggregated_data.values])))

plt.plot(my_zerg_aggregated_data)
plt.plot(pro_zerg_aggregated_data)
score = sum(my_zerg_aggregated_data) / sum(pro_zerg_aggregated_data)

plt.legend(['my creep', 'pro creep'])
plt.title(f"creep ZvZ Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_creep_zvz_benchmark.png")
plt.clf()

my_protoss_df = my_df.query('opponent_race == "Protoss"')
my_protoss_aggregated_data = my_protoss_df.groupby('second')['creep_count'].quantile(0.50)[:-50]
my_protoss_aggregated_data

pro_protoss_df = pro_df.query('opponent_race == "Protoss"')
pro_protoss_aggregated_data = pro_protoss_df.groupby('second')['creep_count'].quantile(0.80)[:-50]
print(",".join(list([str(x) for x in pro_protoss_aggregated_data.values])))

plt.plot(my_protoss_aggregated_data)
plt.plot(pro_protoss_aggregated_data)
score = sum(my_protoss_aggregated_data) / sum(pro_protoss_aggregated_data)

plt.legend(['my creep', 'pro creep'])
plt.title(f"creep ZvP Benchmark - Score {score:.0%}")
plt.savefig(f"png_my_creep_zvp_benchmark.png")
plt.clf()
