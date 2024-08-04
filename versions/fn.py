from config.log_config import logger
import pandas as pd


file_path = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/EET-240604.PSV"

# read one file 
def read_files(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        
    elif file_path.endswith('.PSV'):
        df = pd.read_csv(file_path, sep='|')
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .psv file.")
    
    return df







rf = read_files(file_path)
logger.info(rf)





from typing import Any, Dict, List, Tuple
import pandas as pd
from config.log_config import logger

from Models.model import EET_Data

file_path = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/EET-240604.PSV"


file0 = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP_smple - Copie (2).csv"
file1 = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP_smple - Copie (3).csv"
file2 = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP_smple - Copie.csv"
file4 = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP_smple.csv"
files = [file_path,file0,file1,file2,file4]



# Read file
def read_psv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', skiprows=1)
    return df

# Extract data from file
def extract_data(file_path: str) -> List[EET_Data]:

    df = read_psv(file_path)
    
    # Extracting data by rows
    data_list = []
    for _, row in df.iterrows():
        trading_data = EET_Data(
            TradingDate=row['TradingDate'],
            CellComputerNo=row['CellComputerNo'],
            SiteCarParkNumber=row['SiteCarParkNumber'],
            DateTime=row['DateTime'],
            TicketType=row['TicketType'],
            Entries=row['Entries'],
            Exits=row['Exits']
        )
        data_list.append(trading_data)
    
    return data_list

# filter data by rows
def filter_data_by_row(file_path: str, filter_conditions: Dict[str, Any]) -> List[EET_Data]:
    df = read_psv(file_path)
    for column, value in filter_conditions.items():
        df = df[df[column] == value]
    
    data_list = []
    for _, row in df.iterrows():
        trading_data = EET_Data(
            TradingDate=row['TradingDate'],
            CellComputerNo=row['CellComputerNo'],
            SiteCarParkNumber=row['SiteCarParkNumber'],
            DateTime=row['DateTime'],
            TicketType=row['TicketType'],
            Entries=row['Entries'],
            Exits=row['Exits']
        )
        data_list.append(trading_data)
    
    return data_list

# filter data by column
def filter_data_by_column(file_path: str, columns: List[str]) -> pd.DataFrame:
    df = read_psv(file_path)
    selected_columns = df[columns]
    return selected_columns.to_string(header=False)

def extract_columns(file_path: str) -> pd.DataFrame:

    df = read_psv(file_path)
    selected_columns = df[['TradingDate', 'CellComputerNo', 'SiteCarParkNumber', 'DateTime', 'TicketType', 'Entries', 'Exits']]
    return selected_columns.to_string(header=False)



# Find one value passed as param
def find_one_value(file_path: str, value: Any) -> Tuple[pd.DataFrame, List[str]]:
    df = read_psv(file_path)
    
    # Find rows containing the value
    rows_with_value = df[df.isin([value]).any(axis=1)]
    
    # Find columns containing the value
    columns_with_value = df.columns[df.isin([value]).any()].tolist()
    
    return rows_with_value, columns_with_value



def find_many_values(file_path: str, values: List[Any]) -> Tuple[pd.DataFrame, List[str]]:
    df = read_psv(file_path)
    
    # Find rows containing any of the values
    rows_with_values = df[df.isin(values).any(axis=1)]
    
    # Find columns containing any of the values
    columns_with_values = df.columns[df.isin(values).any()].tolist()
    
    return rows_with_values, columns_with_values

# main:

#extract all data in the file every single data with prefix
""" data_list = extract_data(file_path)
for data in data_list:
    logger.info(f"{data}")
    
    
# extract all data in the file as cols
columns_df = extract_columns(file_path)
logger.info(f" Extract all data in the file as cols \n \n{columns_df} \n")


# Filter by row
row_filters = {
    'DateTime': '04.06.2024 00:00:00',
    'Entries': 0
}

# Filter data by rows
filtered_rows = filter_data_by_row(file_path, row_filters)
for data in filtered_rows:
    logger.info(f" Filter data by rows \n{data} \n")


# Filter by column
columns_to_select = ['TradingDate', 'CellComputerNo', 'SiteCarParkNumber', 'DateTime']
filtered_columns_df = filter_data_by_column(file_path, columns_to_select)
logger.info(f"Filter by column \n{filtered_columns_df} ")


# Find value
value_to_find = 7
rows, columns = find_one_value(file_path, value_to_find)

logger.info(f" Find value \n{rows}")
logger.info(f" Find value {columns} == {value_to_find}") """

"""
values_to_find = ["22:00:00", "5"]

rows_containing_values, columns_with_values = find_many_values(file_path, values_to_find)

logger.info(f" Find many value \n n{rows_containing_values}")
logger.info(f" Find many value {columns_with_values} == {values_to_find}")
"""

mydf =read_psv(file_path)

rest =mydf.query('Exits == 0')
print(rest["TicketType"].sum())