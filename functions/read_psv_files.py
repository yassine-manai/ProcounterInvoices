import os
import pandas as pd
from typing import Dict
from config.log_config import logger


# read file in folder , read all file .psv and return files in folder as dictionary
def read_psv_from_folder(folder_path: str, encoding: str = 'ISO-8859-1') -> Dict[str, pd.DataFrame]:
    
    """
    Reads all .PSV files from a specified folder and returns them as a dictionary of DataFrames.

    This function scans the given folder for files with the .PSV extension, reads each file into
    a pandas DataFrame using the specified encoding, and stores each DataFrame in a dictionary.
    The keys of the dictionary are the file names and the values are the corresponding DataFrames.

    Parameters:
        folder_path (str): The path to the folder containing the .PSV files.
        encoding (str): The character encoding to use when reading the files (default is 'ISO-8859-1').

    Returns:
        Dict[str, pd.DataFrame]: A dictionary where the keys are file names and the values are DataFrames
                                 read from the .PSV files.
    """
    
    df_dict = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.PSV'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, sep='|', skiprows=0, encoding=encoding)
            df_dict[file_name] = df

    return df_dict


def read_file(file_path: str, encoding: str = 'ISO-8859-1') -> pd.DataFrame:
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.psv':
        separator = ';'
    elif file_extension.lower() == '.csv':
        separator = ','
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, sep=separator, skiprows=1,header=0, encoding=encoding)
    
    return df
