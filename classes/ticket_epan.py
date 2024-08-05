import pandas as pd
#from config.log_config import logger

class TicketEpanError(Exception):
    pass

class TicketEpan:
    def __init__(self, ticket_epan):
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



    def validate(self):
        return (
            self.parking.isdigit() and
            self.clientid.isdigit() and
            self.zr_number.isdigit() and
            self.type_parker.isdigit() and
            self.company_id.isdigit() and
            self.ptcpid.isdigit()  
        )

    def to_dict(self):
        return {
            "parking": self.parking,
            "clientid": self.clientid,
            "zr_number": self.zr_number,
            "type_parker": self.type_parker,
            "company_id": self.company_id,
            "ptcpid": self.ptcpid
        }
        



class TicketEPANSummary:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def summarize(self) -> list:
        epan_list = self.dataframe['TicketEPAN'].unique()
        summaries = []
        
        for epan in epan_list:
            #logger.debug(f"Working on Epan = {epan}")
            
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
    
    
