import os
import pandas as pd
from typing import Dict, List


# read file in folder , read all file .psv and return files in folder as dictionary
def read_psv_from_folder(folder_path: str) -> Dict[str, pd.DataFrame]:
    df_dict={}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.PSV'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, sep='|', skiprows=1)
            df_dict[file_name] = df
            
    return df_dict


# read .psv file and return a dataframe object
def read_psv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', skiprows=1)
    return df




