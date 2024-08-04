import pandas as pd
from config.log_config import logger

class FilePPD:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def rslts(self) -> list:
        epan_list = self.dataframe['TicketEPAN'].unique()
        ppd_list = []

        for epan in epan_list:
            logger.debug(f"Working on Epan = {epan}")

            filtered_df = self.dataframe[self.dataframe['TicketEPAN'] == epan]
            if not filtered_df.empty:
                PPD_rslt = {
                    'TranDateTime': filtered_df['TranDateTime'].values,  
                    'Price': filtered_df['Price'].sum().item(),
                    'NetPrice': filtered_df['NetPrice'].sum().item(),
                    'VATAmount': filtered_df['VATAmount'].sum().item(),
                    'VATRate': filtered_df['VATRate'].values[0],  
                    'CurrencyCode': str(filtered_df['CurrencyCode'].iloc[0]),  
                    'Quantity': filtered_df['Quantity'].sum().item(),
                    'TicketEPAN': str(epan),  
                    'TariffStart': filtered_df['TariffStart'].values,  
                    'TariffEnd': filtered_df['TariffEnd'].values
                }
                ppd_list.append(PPD_rslt)

        return ppd_list