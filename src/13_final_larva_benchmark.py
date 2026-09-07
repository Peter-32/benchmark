from utils import *
import pandas as pd
import matplotlib.pyplot as plt

my_df = local.read.csv("12_my_larva_transform", 'interim')
my_terran_df = my_df.query('opponent_race == "Terran"')
my_terran_aggregated_data = my_terran_df.groupby('second')['larva_amount'].quantile(0.50)
my_terran_aggregated_data

pro_df = local.read.csv("12_pro_larva_transform", 'interim')
pro_terran_df = pro_df.query('opponent_race == "Terran"')
pro_terran_aggregated_data = pro_terran_df.groupby('second')['larva_amount'].quantile(0.20)
pro_terran_aggregated_data

plt.plot(my_terran_aggregated_data)
plt.plot(pro_terran_aggregated_data)
score = sum(pro_terran_aggregated_data) / sum(my_terran_aggregated_data)
plt.legend(['my cumulative unspent larva resources', 'pro cumulative larva resources'])
plt.title(f"Larva ZvT Benchmark - Score {score:.0%}")
plt.savefig("../data/output/my_larva_zvt_benchmark.png")
plt.clf()

my_zerg_df = my_df.query('opponent_race == "Zerg"')
my_zerg_aggregated_data = my_zerg_df.groupby('second')['larva_amount'].quantile(0.50)
my_zerg_aggregated_data

pro_zerg_df = pro_df.query('opponent_race == "Zerg"')
pro_zerg_aggregated_data = pro_zerg_df.groupby('second')['larva_amount'].quantile(0.20)
pro_zerg_aggregated_data

plt.plot(my_zerg_aggregated_data)
plt.plot(pro_zerg_aggregated_data)
score = sum(pro_zerg_aggregated_data) / sum(my_zerg_aggregated_data)
plt.legend(['my cumulative unspent larva resources', 'pro cumulative larva resources'])
plt.title(f"Larva ZvZ Benchmark - Score {score:.0%}")
plt.savefig("../data/output/my_larva_zvz_benchmark.png")
plt.clf()

my_protoss_df = my_df.query('opponent_race == "Protoss"')
my_protoss_aggregated_data = my_protoss_df.groupby('second')['larva_amount'].quantile(0.50)
my_protoss_aggregated_data

pro_protoss_df = pro_df.query('opponent_race == "Protoss"')
pro_protoss_aggregated_data = pro_protoss_df.groupby('second')['larva_amount'].quantile(0.20)
pro_protoss_aggregated_data

plt.plot(my_protoss_aggregated_data)
plt.plot(pro_protoss_aggregated_data)
score = sum(pro_protoss_aggregated_data) / sum(my_protoss_aggregated_data)
plt.legend(['my cumulative unspent larva resources', 'pro cumulative larva resources'])
plt.title(f"Larva ZvP Benchmark - Score {score:.0%}")
plt.savefig("../data/output/my_larva_zvp_benchmark.png")
plt.clf()
