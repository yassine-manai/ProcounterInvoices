import csv
from typing import Any, Dict, List, Tuple
import pandas as pd
from datetime import datetime

from classes.ticket_epan import TicketEpanError,TicketEpan
from config.config import ACCOUNT_NUMBER, BIC
from config.log_config import logger

from procountor.api.invoiceGet import get_all_invoice
from procountor.api.invoicePost import create_invoice, create_invoices
from procountor.models.invoice_model import Invoice

from functions.fetch_token import fetch_data_token 
from globalvars.glob_data import token_data

#EET = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/EET-240604.PSV"
#KPI = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/KPI-240605.PSV"



# Read file
def read_psv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', skiprows=1)
    return df


file1 = read_psv("./DEP/PPA-240604.PSV")
#df2 = read_psv(KPI)


#logger.info(f"\n {file1} \n")

#logger.info(f"\n {df2} \n")

rest1 = file1.query('Price == 50')
rest2 = rest1.query('Discounted == "Y"')
#logger.info(f"\n {rest2} \n")

#rest2 = df2.query('SiteCarParkNumber == 1068')

#frames = [rest1, rest2]

#result = rest1.merge(rest2,how='cross')

#logger.info(f"\n {result} \n")

# Specify the path for the output CSV file
#output_file = "/mnt/c/Users/yassi/Desktop/AsteroIdea/Projects Specs/Finland - Procounter Invoicing API Connector/DEP/merged_data.csv"

# Write the merged DataFrame to a new CSV file
#result.to_csv(output_file, index=False)

# Log a message indicating the CSV file has been created
#logger.info(f"Merged data written to {output_file}")

#logger.info(f"\n {rest1[['TradingDate', 'Entries']]}")
#logger.info(f"\n {rest2["DeviceNumber"].count()}")

""" logger.debug("Process start . . . ")
fetch_data_token()
logger.info(f"Token data fetched and saved {token_data}")


logger.info(f"\n Send get invoices request started . . .  \n")
response = get_all_invoice()

if response:
    logger.info(f"Response from the API: {response}")
else:
    logger.error("Failed to create invoice")

"""
 


invoicreee_data = {
    "type": "SALES_INVOICE", 
    "status": "UNFINISHED",
    "date": "2024-07-18", # current date
    "counterParty": {
        "identifier": "42544", # company identifier (CRP file, clm 03)
        "customerNumber": "1122334455", # customer number (CRP file, clm 11)
        "email": "hamza@gmail.com", #Nt Defined
        "counterPartyAddress": {
            "name": "Yassine Manai", # customer name (CRP file, clm 07)
            "specifier": "Megrine",# customer adress (CRP file, clm 11)
            "street": "beja",# customer street (CRP file, clm 08)
            "zip": "2044",# customer zipCode (CRP file, clm 09)
            "city": "Megrine",# customer city (CRP file, clm 10)
        }
    },
    "billingAddress": {
        "name": "Yassine Manai", # customer name (CRP file, clm 07)
        "specifier": "Megrine",# customer adress (CRP file, clm 11)
        "street": "beja",# customer street (CRP file, clm 08)
        "zip": "2044",# customer zipCode (CRP file, clm 09)
        "city": "Megrine",# customer city (CRP file, clm 10)
    },
    "paymentInfo": {
        "paymentMethod": "BANK_TRANSFER",
        "currency": "EUR",
        "bankAccount": {
            "accountNumber": ACCOUNT_NUMBER,
            "bic": BIC
        },
        "dueDate": "2024-07-31", 
        "currencyRate": 1,
        "paymentTermPercentage": 0,
        "bankReferenceCode": "26013",
        "clearingCode": "0"
    },
    "extraInfo": {
        "accountingByRow": True,
        "unitPricesIncludeVat": True
    },
    "discountPercent": 10,
    "orderReference": "",
    "invoiceRows": [
        {
            "product": "Season Parker",  # concat customer name - last name (for every row)
            "productCode": "1145", # extract season parking code from EPAN (PPA file, Clm22)
            "quantity": 2, # sum of rows (PPA file, Clm17)
            "unit": "HOUR", # default HOUR unit
            "unitPrice": 15, # sum of prices by ticket EPAN (PPA file, Clm8)
            "discountPercent": 2, # calculate discount by check (PPA file, Clm12) , if Y the discount = clm13/clm8*100 , if N the discount=0
            "vatPercent": 0, # vat amount (PPA file, Clm23)
            "startDate": "2024-07-18", # company start date (CRP file, Clm28)
            "endDate": "2024-08-18" # company start date (CRP file, Clm29)
        },
    ],
    "vatStatus": 1,
    "deliveryStartDate": "2024-07-31", # passed as params 
    "deliveryEndDate": "2024-08-18", # passed as params 
    "deliveryMethod": "ONLINE",
    "deliveryInstructions": "Nothing",
    "invoiceChannel": "EMAIL",
    "penaltyPercent": 100, # passed as params  
    "language": "ENGLISH", # passed as default 
    "additionalInformation": "Thnks to use our service", # optional
    "notes": "Test information", # optional
    "factoringText": "string", 
    "Number": "55958",
    "agreementNumber": "FIN1447988",
    "version": "2024-07-29T13:04:58.970Z"
}


#response = create_invoices(invoice_data)
""" 
if response:
    logger.info(f"Response from the API: {response}")
else:
    logger.error("Failed to create invoice")

logger.debug("Process stoped. . . ")
  """
 


""" PPA = read_psv("./DEP/PPA-240604.PSV")
CRP = read_psv("./DEP/CRP-240604.PSV")


ticket_epan_series = PPA['TicketEPAN']
payment_number_series = CRP['PaymentNumber']

parsed_ticket_epans = {payment_number: parse_ticket_epan(ticket_epan) 
                       for payment_number, ticket_epan in zip(payment_number_series, ticket_epan_series)}

logger.debug(parsed_ticket_epans)



for epan in parsed_ticket_epans:
    logger.debug(epan) """
    
    

def read_psv(file_path: str, encoding: str = 'ISO-8859-1') -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', skiprows=1, encoding=encoding)
    logger.debug(f"Read {file_path} . . . ")
    return df

""" def process_files(ppa_file_path, crp_file_path, output_csv_path):
    PPA = read_psv(ppa_file_path)
    CRP = read_psv(crp_file_path)
    
    ticket_epan_series = PPA['TicketEPAN']
    parsed_ticket_epans = []
    for idx, (payment_number, ticket_epan) in enumerate(zip(ticket_epan_series)):
        logger.debug(f"Processing row {idx}: PaymentNumber={payment_number}, TicketEPAN={ticket_epan}")
        
        parsed_epan = TicketEpan(ticket_epan)
        logger.debug(f"Parsed EPAN: {parsed_epan}")
        
        company_id = parsed_epan["company_id"]
        logger.debug(f"Company ID: {company_id}")

        # Find the company data in CRP
        company_data = CRP[CRP['Comp_No'] == int(company_id)]
        
        if not company_data.empty:
            company_data = company_data.iloc[0]
            row = {
                "EPAN": ticket_epan,
                **parsed_epan,
                "Comp_No": company_data['Comp_No'],
                "Comp_Name": company_data['Comp_Name'],
                "Comp_ShortName": company_data['Comp_ShortName'],
                "Name2": company_data['Name2'],
                "Street": company_data['Street'],
                "ZipCode": company_data['ZipCode'],
                "City": company_data['City'],
                "Phone": company_data['Phone']
            }
            parsed_ticket_epans.append(row)
        else:
            logger.warning(f"No company data found for company ID: {company_id}")

    logger.debug(f"Total parsed rows: {len(parsed_ticket_epans)}")
    
    # Converting the list of dictionaries to a DataFrame
    df_parsed_ticket_epans = pd.DataFrame(parsed_ticket_epans)
    logger.debug(f"DataFrame shape: {df_parsed_ticket_epans.shape}")
    
    # Saving the processed data to a CSV file
    df_parsed_ticket_epans.to_csv(output_csv_path, index=False)
    logger.success(f"Processed files and saved to {output_csv_path}") """

# File paths
ppa_file_path = "./DEP/PPA-240604.PSV"
crp_file_path = "./DEP/CRP-240604.PSV"
output_csv_path = "./DEP/1file.csv"

# Process the files
#process_files(ppa_file_path, crp_file_path, output_csv_path)

PPA = read_psv(ppa_file_path)
CRP = read_psv(crp_file_path)

date_str = datetime.now().strftime("%Y-%m-%d")
#print (PPA)

epanlist=PPA.TicketEPAN.unique()
for epan in epanlist:
    print(f"Working on Epan = {epan}")
    filtered_df = PPA[PPA['TicketEPAN'] == epan]
    sum_Quantity = filtered_df['Quantity'].sum()
    sum_Price = filtered_df['Price'].sum()
    sum_Turnover = filtered_df['Turnover'].sum()
    sum_NetPrice = filtered_df['NetPrice'].sum()
    sum_NetTurnover = filtered_df['NetTurnover'].sum()
    sum_VATAmount = filtered_df['VATAmount'].sum()
    print(f"{sum_Quantity}-{sum_Price}-{sum_Turnover}-{sum_NetPrice}-{sum_NetTurnover}-{sum_VATAmount}")
    
input()
ticket_epan_series = PPA.get('TicketEPAN','0')
print (f'---{ticket_epan_series}---')

parking = TicketEpan(ticket_epan_series).parking

clientid = TicketEpan(ticket_epan_series).clientid
zr_number = TicketEpan(ticket_epan_series).zr_number
season_parker = TicketEpan(ticket_epan_series).season_parker
company_id = TicketEpan(ticket_epan_series).company_id
ptcpid = TicketEpan(ticket_epan_series).ptcpid


logger.debug(f"Parsed EPAN:{company_id}")

query_id = CRP.query(f'Comp_No == {int(company_id)}')

Phone_Number = query_id.iloc[0]['Phone']
Company_Name = query_id.iloc[0]['Comp_Name']
Street = query_id.iloc[0]['Street']
ZipCode = int(query_id.iloc[0]['ZipCode'])
City = query_id.iloc[0]['City']
ContractStart = query_id.iloc[0]['Comp_ContractStart']
ContractEnd = query_id.iloc[0]['Comp_ContractEnd']
Ptcpt_Surname = query_id.iloc[0]['PTCPT_Surname']


Price = int(PPA['Price'].iloc[0])
NetPrice = int(PPA['NetPrice'].iloc[0])
Quantity = int(PPA['Quantity'].iloc[0])
VATAmount = int(PPA['VATAmount'].iloc[0])
Cancelled = str(PPA['Cancelled'].iloc[0])

print("hello")
print(parking, type(parking))
print(clientid, type(clientid))
print(zr_number, type(zr_number))
print(season_parker, type(season_parker))
print(company_id, type(company_id))
print(ptcpid, type(ptcpid))
print(int(company_id), type(int(company_id)))
print(Phone_Number, type(Phone_Number))
print(Company_Name, type(Company_Name))
print(Street, type(Street))
print(ZipCode, type(ZipCode))
print(City, type(City))
print(ContractStart, type(ContractStart))
print(ContractEnd, type(ContractEnd))
print(Ptcpt_Surname, type(Ptcpt_Surname))
print(Price, type(Price))
print(NetPrice, type(NetPrice))
print(Quantity, type(Quantity))
print(VATAmount, type(VATAmount))
print(Cancelled, type(Cancelled))
print("beslema")


invoice_data = {
    "type": "SALES_INVOICE", 
    "status": "UNFINISHED",
    "date": "2024-07-18",
    "counterParty": {
        "identifier": str(company_id),
        "customerNumber": "122553456",
        "email": "test@mail.com",
        "counterPartyAddress": {
            "name": str(Company_Name),
            "street": str(Street),
            "zip": str(ZipCode),
            "city": str(City),
        }
    },
    "billingAddress": {
        "name": str(Company_Name),
        "street": str(Street),
        "zip": str(ZipCode),
        "city": str(City),
    },
    "paymentInfo": {
        "paymentMethod": "BANK_TRANSFER",
        "currency": "EUR",
        "bankAccount": {
            "accountNumber": str(ACCOUNT_NUMBER),
            "bic": str(BIC)
        },
        "dueDate": "2024-07-31",
        "currencyRate": 1,
        "paymentTermPercentage": 0,
        "bankReferenceCode": "26013",
        "clearingCode": "0"
    },
    "extraInfo": {
        "accountingByRow": True,
        "unitPricesIncludeVat": True
    },
    "discountPercent": 10,
    "orderReference": "",
    "invoiceRows": [
        {
            "product": str(Ptcpt_Surname),
            "productCode": "1145",
            "quantity": float(Quantity),
            "unit": "HOUR",
            "unitPrice": float(NetPrice),
            "discountPercent": 2,
            "vatPercent": 0,
            "startDate": "2024-07-18",
            "endDate": "2024-08-18"
        }
    ],
    "vatStatus": 1,
    "deliveryStartDate": "2024-07-31",
    "deliveryEndDate": "2024-08-18",
    "deliveryMethod": "ONLINE",
    "deliveryInstructions": "Nothing",
    "invoiceChannel": "EMAIL",
    "penaltyPercent": 100,
    "language": "ENGLISH",
    "additionalInformation": "Thanks to use our service",
    "notes": "Test information",
    "factoringText": "string",
    "number": "55958",
    "agreementNumber": "FIN147988",
    "version": "2024-07-30T15:04:58.970Z"
}


""" print("\n")

fetch_data_token()
logger.info(f"Token data fetched and saved {token_data}")
print("\n")

response = create_invoices(invoice_data)

if response:
    logger.info(f"Response from the API: {response}")
else:
    logger.error("Failed to create invoice")

logger.debug("Process stoped. . . ")

  
try:
    parsed_epan = TicketEpan(ticket_epan_series).clientid
    #logger.debug(f"Parsed EPAN:{int(parsed_epan)}")
    
    query_id = CRP.query(f'Comp_No == {int(parsed_epan)}')
    
    


    
except TicketEpanError as e:
    logger.error(f"Error parsing TicketEPAN: {e}") """