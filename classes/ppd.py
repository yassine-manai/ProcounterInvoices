import pandas as pd
from config.log_config import logger

class FilePPD:
    """
    A class to process and extract unique ticket information from a DataFrame.

    Attributes:
        dataframe (pd.DataFrame): The DataFrame containing ticket data.
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Constructs all the necessary attributes for the FilePPD object.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame containing ticket data.
        """
        self.dataframe = dataframe

    def rslts(self) -> list:
        """
        Processes the DataFrame to extract and summarize unique ticket information.

        This method filters the DataFrame for each unique 'TicketEPAN' value,
        aggregates the relevant data, and returns a list of dictionaries containing
        summarized information for each 'TicketEPAN'.

        Returns:
            list: A list of dictionaries, each containing summarized ticket data for a unique 'TicketEPAN'.
        """
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
