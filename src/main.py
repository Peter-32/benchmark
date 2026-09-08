import subprocess
import sys
from glob import glob
import tqdm

all_files = glob("*.py")
files_of_interest = [y for (x, y) in sorted([(str(x.split("_")[0]).zfill(2), x) for x in all_files]) if 'get_data' not in y and 'pro' not in y and y not in ['main.py', 'utils.py']]
replay_path = r'C:\Users\peter\OneDrive\code\benchmark\data\input\my_data\sample_1'
player_name = 'nemo'
subprocess.run([sys.executable, '1_get_data.py', replay_path, player_name])
for script_name in tqdm.tqdm(files_of_interest):
    print(script_name)
    subprocess.run([sys.executable, script_name])