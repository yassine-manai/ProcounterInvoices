import pandas as pd
# from config.log_config import logger

class TicketEpanError(Exception):
    """
    Custom exception class for TicketEpan validation errors.
    """
    pass

class TicketEpan:
    """
    A class to parse and validate TicketEPAN strings.

    Attributes:
        parking (str): Parking identifier.
        clientid (str): Client identifier.
        zr_number (str): ZR number.
        type_parker (str): Type parker.
        company_id (str): Company identifier.
        ptcpid (str): PTCP identifier.
    """
    
    def __init__(self, ticket_epan: str):
        """
        Constructs all the necessary attributes for the TicketEpan object.

        Parameters:
            ticket_epan (str): The TicketEPAN string to be parsed.

        Raises:
            TicketEpanError: If the ticket_epan is not a string or is too short.
        """
        if not isinstance(ticket_epan, str):
            raise TicketEpanError("ticket_epan must be a string")
        
        if len(ticket_epan) < 18:
            raise TicketEpanError("ticket_epan string is too short")
        
        self.parking = ticket_epan[:2]
        self.clientid = ticket_epan[2:7]
        self.zr_number = ticket_epan[7:11]
        self.type_parker = ticket_epan[11:13]
        self.company_id = ticket_epan[13:18]
        self.ptcpid = ticket_epan[18:23]

    def validate(self) -> bool:
        """
        Validates the parsed TicketEPAN components to ensure they are all digits.

        Returns:
            bool: True if all components are valid, False otherwise.
        """
        return (
            self.parking.isdigit() and
            self.clientid.isdigit() and
            self.zr_number.isdigit() and
            self.type_parker.isdigit() and
            self.company_id.isdigit() and
            self.ptcpid.isdigit()
        )

    def to_dict(self) -> dict:
        """
        Converts the TicketEPAN components to a dictionary.

        Returns:
            dict: A dictionary representation of the TicketEPAN components.
        """
        return {
            "parking": self.parking,
            "clientid": self.clientid,
            "zr_number": self.zr_number,
            "type_parker": self.type_parker,
            "company_id": self.company_id,
            "ptcpid": self.ptcpid
        }

class TicketEPANSummary:
    """
    A class to summarize TicketEPAN data from a DataFrame.

    Attributes:
        dataframe (pd.DataFrame): The DataFrame containing TicketEPAN data.
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Constructs all the necessary attributes for the TicketEPANSummary object.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame containing TicketEPAN data.
        """
        self.dataframe = dataframe

    def summarize(self) -> list:
        """
        Summarizes the TicketEPAN data by calculating the sums of various columns for each unique TicketEPAN.

        Returns:
            list: A list of dictionaries, each containing summarized data for a unique TicketEPAN.
        """
        epan_list = self.dataframe['TicketEPAN'].unique()
        summaries = []
        
        for epan in epan_list:
            # logger.debug(f"Working on Epan = {epan}")
            
            filtered_df = self.dataframe[self.dataframe['TicketEPAN'] == epan]
            summary = {
                'epan': epan,
                'sum_Quantity': int(filtered_df['Quantity'].sum()),
                'sum_Price': int(filtered_df['Price'].sum()),
                'sum_Turnover': int(filtered_df['Turnover'].sum()),
                'sum_NetPrice': int(filtered_df['NetPrice'].sum()),
                'sum_NetTurnover': int(filtered_df['NetTurnover'].sum()),
                'sum_VATAmount': int(filtered_df['VATAmount'].sum())
            }
            summaries.append(summary)
        
        return summaries
