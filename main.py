import csv
from typing import Any, Dict, List, Tuple
import pandas as pd
from config.log_config import logger

from Models.model import EET_Data

EET = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/EET-240604.PSV"
KPI = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/KPI-240605.PSV"



# Read file
def read_psv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', skiprows=1)
    return df


df1 = read_psv(EET)
df2 = read_psv(KPI)


#logger.info(f"\n {df1} \n")

#logger.info(f"\n {df2} \n")

rest1 = df1.query('TradingDate == "05.06.2024"')
rest2 = df2.query('SiteCarParkNumber == 1068')


frames = [rest1, rest2]

result = rest1.merge(rest2,how='cross')

logger.info(f"\n {result} \n")

# Specify the path for the output CSV file
output_file = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/merged_data.csv"

# Write the merged DataFrame to a new CSV file
result.to_csv(output_file, index=False)

# Log a message indicating the CSV file has been created
logger.info(f"Merged data written to {output_file}")



#logger.info(f"\n {rest1[['TradingDate', 'Entries']]}")
#logger.info(f"\n {rest2["DeviceNumber"].count()}")