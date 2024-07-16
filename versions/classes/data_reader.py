import pandas as pd
import glob
import os
from typing import List, Optional, Union, Dict
from config.log_config import logger

class dataReader:
    def __init__(self):
        self.default_encodings = ['utf-8', 'iso-8859-1', 'latin1', 'cp1252']

    def read_single_file(self, file_path: str, encoding: Optional[str] = None, **kwargs) -> Optional[pd.DataFrame]:
        """
        Read a single CSV file and return its contents as a DataFrame.

        :param file_path: Path to the CSV file
        :param encoding: Encoding to use for reading the file
        :param kwargs: Additional arguments to pass to pd.read_csv
        :return: DataFrame or None if file couldn't be read
        """
        encodings_to_try = [encoding] if encoding else self.default_encodings

        for enc in encodings_to_try:
            try:
                logger.info(f"Attempting to read file with encoding: {enc}")
                df = pd.read_csv(file_path, encoding=enc, **kwargs)
                
                logger.info(f"Successfully read file with encoding: {enc}")
                logger.debug(f"Fetched data from the file : \n{df.head()}")
                
                return df
            except UnicodeDecodeError:
                logger.warning(f"UnicodeDecodeError with encoding {enc}")
            except Exception as e:
                logger.error(f"Error reading file with encoding {enc}: {str(e)}")

        logger.error(f"Failed to read the file {file_path} with any of the specified encodings")
        return None

    def read_multiple_files(self, 
                            file_paths: Union[str, List[str]], 
                            encoding: Optional[str] = None,
                            columns: Optional[List[str]] = None,
                            data_types: Optional[Dict] = None,
                            chunk_size: Optional[int] = None,
                            skip_errors: bool = False) -> List[Dict[str, Union[str, pd.DataFrame]]]:
        """
        Read multiple CSV files and return a list of dictionaries containing file names and their data.

        :param file_paths: A string (glob pattern) or list of file paths
        :param encoding: Encoding to use for reading CSV files
        :param columns: List of columns to use (if not all columns are needed)
        :param data_types: Dictionary of column data types
        :param chunk_size: Number of rows to read at a time (for large files)
        :param skip_errors: If True, skip files that cause errors
        :return: List of dictionaries with file names and their corresponding DataFrames
        """
        result = []

        if isinstance(file_paths, str):
            file_paths = glob.glob(file_paths)

        for file_path in file_paths:
            try:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                logger.info(f"Reading file: {file_path}")

                if chunk_size:
                    chunks = []
                    for chunk in pd.read_csv(file_path, encoding=encoding, usecols=columns, 
                                             dtype=data_types, chunksize=chunk_size):
                        chunks.append(chunk)
                    df = pd.concat(chunks, ignore_index=True)
                else:
                    df = self.read_single_file(file_path, encoding=encoding, usecols=columns, dtype=data_types)

                if df is not None:
                    result.append({"file_name": os.path.basename(file_path), "data": df})
                    logger.info(f"Successfully read {len(df)} rows from {file_path}")
                else:
                    logger.warning(f"Failed to read file: {file_path}")

            except Exception as e:
                error_msg = f"Error reading file {file_path}: {str(e)}"
                if skip_errors:
                    logger.warning(error_msg)
                else:
                    logger.error(error_msg)
                    raise

        if not result:
            logger.warning("No valid data read from any files.")

        return result

    def combine_dataframes(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Combine multiple DataFrames into a single DataFrame.

        :param dataframes: List of DataFrames to combine
        :return: Combined DataFrame
        """
        return pd.concat(dataframes, ignore_index=True)

# Example usage:
# reader = DataReader()
# files = ["/path/to/file1.csv", "/path/to/file2.csv"]
# result = reader.read_multiple_files(files)
# if result:
#     for file_data in result:
#         print(f"File: {file_data['file_name']}")
#         print(file_data['data'].head())
#         print("\n")
# else:
#     print("No data was read from the files.")