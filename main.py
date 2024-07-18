import csv
from typing import Any, Dict, List, Tuple
import pandas as pd
import requests
from config.config import PROCOUNTOR_URL
from config.log_config import logger

from procountor.api.invoicePost import create_invoice
from procountor.models.invoice_model import Invoice

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

invoice_data = Invoice(
    partnerId=0,
    type="SALES_INVOICE",
    status="UNFINISHED",
    date="2024-07-18",
    counterParty={
        "contactPersonName": "string",
        "identifier": "string",
        "taxCode": "string",
        "customerNumber": "string",
        "email": "string",
        "counterPartyAddress": {
            "name": "string",
            "specifier": "string",
            "street": "string",
            "zip": "string",
            "city": "string",
            "country": "SWEDEN",
            "subdivision": "string"
        },
        "bankAccount": {
            "accountNumber": "string",
            "bic": "string"
        },
        "einvoiceAddress": {
            "operator": "string",
            "address": "string",
            "ediId": "string"
        }
    },
    billingAddress={
        "name": "string",
        "specifier": "string",
        "street": "string",
        "zip": "string",
        "city": "string",
        "country": "SWEDEN",
        "subdivision": "string"
    },
    deliveryAddress={
        "name": "string",
        "specifier": "string",
        "street": "string",
        "zip": "string",
        "city": "string",
        "country": "SWEDEN",
        "subdivision": "string"
    },
    paymentInfo={
        "paymentMethod": "BANK_TRANSFER",
        "currency": "EUR",
        "bankAccount": {
            "accountNumber": "string",
            "bic": "string"
        },
        "dueDate": "2024-07-18",
        "currencyRate": 1,
        "paymentTermPercentage": 0,
        "cashDiscount": {
            "optionList": [
                {
                    "numberOfDays": 0,
                    "discountPercentage": 0
                }
            ],
            "cashDiscountsTermType": "FROM_INV_DATE"
        },
        "bankReferenceCode": "26013",
        "bankReferenceCodeType": "RF",
        "clearingCode": "string"
    },
    deliveryTermsInfo={
        "name": "string",
        "municipality": "string"
    },
    extraInfo={
        "accountingByRow": True,
        "unitPricesIncludeVat": True
    },
    discountPercent=0,
    orderReference="string",
    invoiceRows=[
        {
            "productId": 0,
            "product": "string",
            "productCode": "string",
            "quantity": 0,
            "unit": "CM",
            "unitPrice": 0,
            "discountPercent": 0,
            "vatPercent": 0,
            "vatStatus": 0,
            "comment": "string",
            "startDate": "2024-07-18",
            "endDate": "2024-07-18",
            "headerText": "string",
            "explanationText": "string"
        }
    ],
    vatStatus=0,
    originalInvoiceNumber="string",
    deliveryStartDate="2024-07-18",
    deliveryEndDate="2024-07-18",
    deliveryMethod="MAILING",
    deliveryInstructions="string",
    invoiceChannel="EMAIL",
    penaltyPercent=0,
    language="ENGLISH",
    invoiceTemplateId=0,
    additionalInformation="string",
    vatCountry="SWEDEN",
    notes="string",
    factoringContractId=0,
    factoringText="string",
    travelInformationItems=[
        {
            "departure": "string",
            "arrival": "string",
            "places": "string",
            "purpose": "string"
        }
    ],
    invoiceApprovalInformation={
        "acceptors": [
            {
                "userId": 0
            }
        ],
        "verifiers": [
            {
                "userId": 0
            }
        ]
    },
    orderNumber="string",
    agreementNumber="string",
    accountingCode="string",
    deliverySite="string",
    tenderReference="string",
    version="2024-07-18T13:04:58.970Z",
    isOffer=True
)

#response = create_invoice(invoice_data)


response = create_invoice(invoice_data)

if response:
    logger.info(f"Response from the API: {response}")
else:
    logger.error("Failed to create invoice")

logger.debug("Process stoped. . . ")
