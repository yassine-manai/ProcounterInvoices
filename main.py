import csv
from typing import Any, Dict, List, Tuple
import pandas as pd
import requests
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

logger.debug("Process start . . . ")
fetch_data_token()
logger.info(f"Token data fetched and saved {token_data}")


logger.info(f"\n Send get invoices request started . . .  \n")
response = get_all_invoice()

if response:
    logger.info(f"Response from the API: {response}")
else:
    logger.error("Failed to create invoice")

logger.debug("Process stoped. . . ")
 


invoice_data = {
    "type": "SALES_INVOICE",
    "status": "UNFINISHED",
    "date": "2024-07-18",
    "counterParty": {
        "contactPersonName": "Hamza Hamez",
        "identifier": "42544",
        "customerNumber": "1122334455",
        "email": "hamza@gmail.com",
        "counterPartyAddress": {
            "name": "Yassine Manai",
            "specifier": "Megrine",
            "street": "beja",
            "zip": "2044",
            "city": "Megrine",
            "country": "TUNISIA",
            "subdivision": "BenArous"
        },
        "einvoiceAddress": {
            "operator": "string",
            "address": "string",
            "ediId": "string"
        }
    },
    "billingAddress": {
        "name": "Hamza",
        "specifier": "Megrine",
        "street": "beja",
        "zip": "2044",
        "city": "Megrine",
        "country": "TUNISIA",
    },
    "deliveryAddress": {
        "name": "Hamza",
        "specifier": "Megrine",
        "street": "beja",
        "zip": "2044",
        "city": "Megrine",
        "country": "TUNISIA",
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
            "product": "Season Parker",
            "productCode": "1145",
            "quantity": 2,
            "unit": "HOUR",
            "unitPrice": 15,
            "discountPercent": 2,
            "vatPercent": 0,
            "startDate": "2024-07-18",
            "endDate": "2024-08-18"
        },
        {
            "product": "Short Term Park",
            "productCode": "1911",
            "quantity": 2,
            "unit": "HOUR",
            "unitPrice": 18,
            "discountPercent": 2,
            "vatPercent": 0,
            "startDate": "2024-07-18",
            "endDate": "2024-08-18"
        },
        {
            "product": "UnderGround Park",
            "productCode": "371",
            "quantity": 14,
            "unit": "HOUR",
            "unitPrice": 14,
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
    "additionalInformation": "Thnks to use our service",
    "notes": "Test information",
    "factoringText": "string",
    "travelInformationItems": [
        {
            "departure": "USA",
            "arrival": "TUN",
            "places": "2",
            "purpose": "Travel"
        }
    ],
    "Number": "5598",
    "agreementNumber": "FIN1447988",
    "version": "2024-07-29T13:04:58.970Z"
}

#response = create_invoice(invoice_data)


response = create_invoices(invoice_data)

if response:
    logger.info(f"Response from the API: {response}")
else:
    logger.error("Failed to create invoice")

logger.debug("Process stoped. . . ")
 
 
