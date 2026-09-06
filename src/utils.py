import pandas as pd; from datetime import datetime
import re; import json; import pickle
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

        @staticmethod
        def tsv(file_name: str, file_type='input', skip_rows=0):
            """Pass the file name and which data subfolder to look to get a dataframe."""
            file_name = file_name if file_name.endswith(".tsv") else file_name + ".tsv" # Adds the .tsv if it is missing
            full_path = local._get_full_path(file_name, file_type)
            return pd.read_csv(full_path, skiprows=skip_rows, sep="\t")

        @staticmethod
        def xls(file_name: str, sheet_name: str, file_type='input', skip_rows=0):
            """Pass the file name, sheet name, and which data subfolder to look to get a dataframe."""
            file_name = file_name if file_name.endswith(".xls") else file_name + ".xls" # Adds the .xls if it is missing
            full_path = local._get_full_path(file_name, file_type)
            return pd.read_excel(full_path, sheet_name, skiprows=skip_rows)

        @staticmethod
        def xlsx(file_name: str, sheet_name: str, file_type='input', skip_rows=0):
            """Pass the file name, sheet name, and which data subfolder to look to get a dataframe."""
            file_name = file_name if file_name.endswith(".xlsx") else file_name + ".xlsx" # Adds the .xlsx if it is missing
            full_path = local._get_full_path(file_name, file_type)
            return pd.read_excel(full_path, sheet_name, skiprows=skip_rows)

        @staticmethod
        def json(file_name: str, file_type='input'):
            """Pass the file name and which data subfolder to look to get a dataframe."""
            file_name = file_name if file_name.endswith(".json") else file_name + ".json" # Adds the .json if it is missing
            full_path = local._get_full_path(file_name, file_type)
            return pd.read_json(full_path, orient="columns")

        @staticmethod
        def parquet(file_name: str, file_type='input'):
            """Pass the file name and which data subfolder to look to get a dataframe."""
            full_path = local._get_full_path(file_name, file_type)
            full_path = full_path if os.path.isdir(full_path) or file_name.endswith(".parquet") else full_path + ".parquet" # Adds the .parquet if it is missing
            return pd.read_parquet(full_path)

        @staticmethod
        def python_object(file_name: str, file_type='interim'):
            """Pass the file name and which data subfolder to look to get a python variable or object."""
            file_name = file_name if file_name.endswith(".pkl") or file_name.endswith(".pickle") or file_name.endswith(".p") else file_name + ".pkl" # Adds the .pkl if it is missing
            full_path = local._get_full_path(file_name, file_type)
            with open(full_path, 'rb') as file:
                return pickle.load(file)
            
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
        def xlsx(dfs: list[pd.DataFrame], sheet_names: list[str], file_name: str, file_type='interim'):
            """Save a list of dataframes to Excel.  Each dataframe goes on a new sheet.  Saved locally in a data subfolder."""
            file_name = file_name if file_name.endswith(".xlsx") else file_name + ".xlsx" # Adds the .xlsx if it is missing
            full_path = local._get_full_path(file_name, file_type)
            with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
                for i in range(len(dfs)):
                    dfs[i].to_excel(writer, sheet_name=sheet_names[i], index=False)               
        
        @staticmethod
        def parquet(df: pd.DataFrame, file_name: str, file_type='interim', is_append=False):
            """Save a dataframe to a parquet file locally in a data subfolder."""
            if not is_append:
                file_name = file_name if file_name.endswith(".parquet") else file_name + ".parquet" # Adds the .parquet if it is missing
            full_path = local._get_full_path(file_name, file_type)
            if is_append:
                if file_name.endswith(".parquet"):
                    raise Exception('Please remove the ".parquet" extension when using append mode.')
                Path(full_path).mkdir(parents=True, exist_ok=True)
                found_files = [x for x in os.listdir(full_path) if x.endswith(".parquet") and x[:-8].isdigit()]
                max_file = '0000000.parquet' if len(found_files) == 0 else max(found_files)
                new_file_name = str(int(max_file[:-8]) + 1).zfill(7) + ".parquet"
                full_path = os.path.join(full_path, new_file_name)
            df.to_parquet(full_path)
        
        @staticmethod
        def python_object(python_object: any, file_name, file_type='interim'):
            """Pass the file name and which data subfolder to save a python variable or object."""
            file_name = file_name if file_name.endswith(".pkl") or file_name.endswith(".pickle") or file_name.endswith(".p") else file_name + ".pkl" # Adds the .pkl if it is missing
            full_path = local._get_full_path(file_name, file_type)
            with open(full_path, 'wb') as file:
                return pickle.dump(python_object, file)

    @staticmethod
    def _get_full_path(file_name: str, file_type: str):
        """This helper function finds the path to your data folder and file_type subfolder (creates the subfolder if needed).
        Places the data folder outside the src/adhoc/notebooks directory of this script/notebook if found otherwise in the same directory."""        
        script_dir = os.path.abspath(os.getcwd())
        base_project_folder = re.split('[/\\\\]+(?:src|adhoc|notebooks)(?:[/\\\\]|$)', script_dir)[0]
        if file_type == 'output':
            file_name = datetime.now().strftime("%Y%m%d_%H%M") + file_name          
        building_path = os.path.join(base_project_folder, "data", file_type)
        Path(building_path).mkdir(parents=True, exist_ok=True)
        full_path = os.path.join(building_path, file_name)
        return full_path