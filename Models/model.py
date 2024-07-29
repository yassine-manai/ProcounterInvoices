from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from pydantic import BaseModel


class ProcountorAPIError(Exception):
    message: str = ""
    status_code: int = None
    response_content: Any = None
    
    
class EET_Data(BaseModel):
    """
    Pydantic model for EET (Event Entry and Exit) data.
    
    Attributes:
    - trading_date: Date of the trading.
    - cell_computer_no: Number of the cell computer.
    - site_car_park_number: Number of the site's car park.
    - date_time: Date and time of the event.
    - ticket_type: Type of ticket related to the event.
    - entries: Number of entries during the event.
    - exits: Number of exits during the event.
    """
    
    TradingDate: str
    CellComputerNo: int
    SiteCarParkNumber: int
    DateTime: str 
    TicketType: int
    Entries: int
    Exits: int
    
 
class CAP_Data(BaseModel):
    TradingDate: str
    CellComputerNo: str
    SiteCarParkNumber: str
    ProductionNumber: str
    PaymentNumber: str
    ProductionDateTime: str
    Device: str
    TicketType: str
    TicketSubType: str
    ParkingArticle: str
    Quantity: str
    Amount: str
    BookedValue: str
    EPAN: str
    ShiftID: str
    Cashier: str
    InvoiceReference: str
    ParkingArtName: str
    ValidDate: str

class CAS_Data(BaseModel):
    trading_date: date
    cell_computer_no: int
    site_car_park_number: int
    start_time: time
    end_time: time
    shift: str
    device: str
    transaction_time: datetime
    cs_type: int
    cs_type_name: str
    money_value: Decimal
    quantity: int
    amount: Decimal
    art_ref_no: str
    art_text: str


class CRC_Data(BaseModel):
    trading_date: datetime
    cell_computer_no: int
    site_car_park_number: int
    payment_number: int
    device_number: int
    tran_date_time: datetime
    credit_card_company: str
    turnover: Decimal
    cancelled: bool
    ident_type: str
    masked_pan: str
    credit_card_no: str
    expiry: str
    card_medium: str
    sb_trans_id: int
    host_approval: bool
    authorization_time: datetime
    booking_time: datetime
    ticket_e_pan: str
    stan: int
    shift_id: int
    batch_id: int
    terminal_id: int
    authorization: bool
    host_trans_id: int
    clearing: bool
    merchant_id: str
    surcharge_amt: Decimal
    
    
class EET_Data(BaseModel):
    trading_date: datetime
    cell_computer_no: int
    site_car_park_number: int
    date_time: datetime
    ticket_type: int
    entries: int
    exits: int
    
class CRP_Data(BaseModel):
    trading_date: datetime
    cell_computer_no: int
    comp_no: int
    comp_name: str
    comp_short_name: str
    salutation: str
    name2: str
    street: str
    zip_code: str
    city: str
    phone: str
    telefax: str
    invoicing_group: int
    invoicing_typ: int
    comp_remove: int
    status: int
    group_count: int
    invoice_memo: str
    payment: int
    comp_month_lump_sum: int
    pay_type: int
    deposit: int
    comp_limit: int
    bank: str
    bank_code: str
    account_no: str
    contract_no: str
    comp_contract_start: datetime
    comp_contract_end: datetime
    ptcpt_no: int
    ptcpt_group_no: int
    ptcpt_surname: str
    ptcpt_first_name: str
    ptcpt_remove: int
    ptcpt_count: int
    ptcpt_blocked: int
    matchcode: str
    ptcpt_memo: str
    lpn_1: str
    lpn_2: str
    lpn_3: str
    park_space_no: int
    facility_key: str
    card_no: str
    prod_time: str
    prod_count: int
    ptcpt_contract_start: datetime
    ptcpt_contract_end: datetime
    ptcpt_limit: int
    ptcpt_month_lump_sum: int
    calc_month_lump_sum_first: int
    week_profile: int
    admission: int
    calculation: int
    overdraft: int
    balance: int
    ptc_free1: str
    ptc_free2: str
    ptc_free3: str
    comp_free1: str
    comp_free2: str
    comp_free3: str
    card_type: int
    
    

class EVT_Data(BaseModel):
    trading_date: datetime
    cell_computer_no: int
    site_car_park_number: int
    device: int
    event_date: datetime
    event_number: int
    event_desc: str 