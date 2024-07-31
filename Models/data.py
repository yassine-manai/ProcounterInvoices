from pydantic import BaseModel


class EET_Data(BaseModel):
    TradingDate: str
    CellComputerNo: int
    SiteCarParkNumber: int
    DateTime: str 
    TicketType: int
    Entries: int
    Exits: int