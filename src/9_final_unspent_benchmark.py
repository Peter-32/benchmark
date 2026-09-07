from utils import *
import pandas as pd
import matplotlib.pyplot as plt

my_df = local.read.csv("4_my_inject_transform", 'interim')
my_terran_df = my_df.query('opponent_race == "Terran"')
my_terran_aggregated_data = my_terran_df.groupby('second')['inject_count'].quantile(0.50)
my_terran_aggregated_data

pro_df = local.read.csv("4_pro_inject_transform", 'interim')
pro_terran_df = pro_df.query('opponent_race == "Terran"')
pro_terran_aggregated_data = pro_terran_df.groupby('second')['inject_count'].quantile(0.80)
pro_terran_aggregated_data

plt.plot(my_terran_aggregated_data)
plt.plot(pro_terran_aggregated_data)
plt.legend(['my injects', 'pro injects'])
plt.title("Inject ZvT Benchmark")
plt.savefig("../data/output/my_inject_zvt_benchmark.png")
plt.clf()

my_zerg_df = my_df.query('opponent_race == "Zerg"')
my_zerg_aggregated_data = my_zerg_df.groupby('second')['inject_count'].quantile(0.50)
my_zerg_aggregated_data

pro_zerg_df = pro_df.query('opponent_race == "Zerg"')
pro_zerg_aggregated_data = pro_zerg_df.groupby('second')['inject_count'].quantile(0.80)
pro_zerg_aggregated_data

plt.plot(my_zerg_aggregated_data)
plt.plot(pro_zerg_aggregated_data)
plt.legend(['my injects', 'pro injects'])
plt.title("Inject ZvZ Benchmark")
plt.savefig("../data/output/my_inject_zvz_benchmark.png")
plt.clf()

my_protoss_df = my_df.query('opponent_race == "Protoss"')
my_protoss_aggregated_data = my_protoss_df.groupby('second')['inject_count'].quantile(0.50)
my_protoss_aggregated_data

pro_protoss_df = pro_df.query('opponent_race == "Protoss"')
pro_protoss_aggregated_data = pro_protoss_df.groupby('second')['inject_count'].quantile(0.80)
pro_protoss_aggregated_data

plt.plot(my_protoss_aggregated_data)
plt.plot(pro_protoss_aggregated_data)
plt.legend(['my injects', 'pro injects'])
plt.title("Inject ZvP Benchmark")
plt.savefig("../data/output/my_inject_zvp_benchmark.png")
plt.clf()
