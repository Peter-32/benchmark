import subprocess
import sys
from glob import glob

all_files = glob("*.py")
print([y for (x, y) in sorted([(str(x.split("_")[0]).zfill(2), x) for x in all_files]) if 'get_data' not in y and 'pro' not in y and y not in ['main.py', 'utils.py']])

# subprocess.run([sys.executable, script_name])