import pandas as pd; from datetime import datetime
import re; import json; import pickle; import sys
import os; import shutil; from pathlib import Path; 
import urllib.parse; import configparser; from functools import lru_cache 
config = configparser.ConfigParser()
config.read('config.ini')

class local:
    """Read and write with local files."""
    class read:
        """Read from project_folder/data/file_type."""
        @staticmethod
        def csv(file_name: str, file_type='input', skip_rows=0):
            """Pass the file name and which data subfolder to look to get a dataframe."""
            file_name = file_name if file_name.endswith(".csv") else file_name + ".csv" # Adds the .csv if it is missing
            full_path = local._get_full_path(file_name, file_type)
            return pd.read_csv(full_path, skiprows=skip_rows)

    class write:
        """Write to project_folder/data/file_type"""
        @staticmethod
        def csv(df: pd.DataFrame, file_name: str, file_type='interim', is_append=False):
            """Save a dataframe to a CSV file locally in a data subfolder."""
            file_name = file_name if file_name.endswith(".csv") else file_name + ".csv" # Adds the .csv if it is missing
            full_path = local._get_full_path(file_name, file_type)
            mode = 'a' if is_append else 'w'
            header = False if is_append else True
            df.to_csv(full_path, mode=mode, header=header, index=False)

    @staticmethod
    def _get_full_path(file_name: str, file_type: str):
        """This helper function finds the path to your data folder and file_type subfolder (creates the subfolder if needed).
        Places the data folder outside the src/adhoc/notebooks directory of this script/notebook if found otherwise in the same directory."""        
        if hasattr(sys, '_MEIPASS'):
            base_project_folder = Path(sys._MEIPASS)
        else:
            script_dir = os.path.abspath(os.getcwd())        
            base_project_folder = re.split('[/\\\\]+(?:src|adhoc|notebooks)(?:[/\\\\]|$)', script_dir)[0]
        if file_type == 'output':
            file_name = datetime.now().strftime("%Y%m%d_%H%M") + file_name          
        building_path = os.path.join(base_project_folder, "data", file_type)
        Path(building_path).mkdir(parents=True, exist_ok=True)
        full_path = os.path.join(building_path, file_name)
        return full_path

def get_base_project_folder():
    if hasattr(sys, '_MEIPASS'):
        base_project_folder = Path(sys._MEIPASS)
    else:
        script_dir = os.path.abspath(os.getcwd())        
        base_project_folder = re.split('[/\\\\]+(?:src|adhoc|notebooks)(?:[/\\\\]|$)', script_dir)[0]
    return base_project_folder