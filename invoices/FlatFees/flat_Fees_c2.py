import glob as gl, pandas as pd
from collections import defaultdict
from functions.data_format import date_format
from classes.ticket_epan import TicketEpan
from config.config import ACCOUNT_NUMBER, BIC
from config.log_config import logger
from functions.discount_fn import calculate_discount_percentage
from procountor.api.invoicePost import create_invoices
from functions.read_psv_files import read_file
from functions.fetch_token import fetch_data_token 
from collections import defaultdict


def flatFee_c2(date_str,ppa_c2,crp_c2):
    
    """
        Processes monthly invoicing by reading data from PPA and CRP files, aggregating ticket information, and creating invoices.

        The function performs the following steps:
        1. Reads and concatenates PPA and CRP data from multiple files.
        2. Fetches and logs token data for API authentication.
        3. Groups tickets by company using the TicketEPAN field.
        4. For each company, retrieves relevant information and constructs invoice data.
        5. Aggregates ticket data for the month, calculates discounts, and creates invoice rows.
        6. Calls an external API to create invoices and logs the response.

        Parameters:
            date_str (str): The date string to be used in the invoice.
            ppa_c2 (str): File path pattern for PPA files (e.g., 'path/to/ppa/files/*.psv').
            crp_c2 (str): File path pattern for CRP files (e.g., 'path/to/crp/files/*.psv').

        Returns:
            None

        Raises:
            Exception: Logs errors if any issues occur while fetching data or creating invoices.
    """
    
    logger.info("Starting Process for monthly invoicing . . . . . . . . . . . . . . . . . . . . .")

    # Read data from all PPA files
    logger.debug(f"Reading PPA files from {ppa_c2}")
    ppa_files = gl.glob(ppa_c2)
    PPA = pd.concat([read_file(file) for file in ppa_files], ignore_index=True)

    # Read data from all CRP files
    logger.debug(f"Reading CRP files from {crp_c2}")
    crp_files = gl.glob(crp_c2)
    CRP = pd.concat([read_file(file) for file in crp_files], ignore_index=True)

    # Fetch and log token data
    fetch_data_token()
    logger.info("Token data fetched and saved")    

    # Process PPA tickets
    epanlist = PPA.TicketEPAN.unique()
    logger.debug(f"Unique EPANs found: {len(epanlist)}")

    company_epans = defaultdict(list)
    for epan in epanlist:
        ticket_epan = TicketEpan(epan)
        company_epans[int(ticket_epan.company_id)].append(epan)

    # Create invoices
    for company_id, epans in company_epans.items():
        invoice_data = {
            "type": "SALES_INVOICE", 
            "status": "UNFINISHED",
            "date": str(date_str),
            "counterParty": {},
            "billingAddress": {},
            "paymentInfo": {
                "paymentMethod": "BANK_TRANSFER",
                "currency": "EUR",
                "bankAccount": {
                    "accountNumber": str(ACCOUNT_NUMBER),
                    "bic": str(BIC)
                },
                "dueDate": "2024-08-22",
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
            "invoiceRows": [],
            "vatStatus": 1,
            "deliveryStartDate": "2024-07-31",
            "deliveryEndDate": "2024-08-18",
            "deliveryMethod": "ONLINE",
            "deliveryInstructions": "Nothing",
            "invoiceChannel": "EMAIL",
            "language": "ENGLISH",
            "additionalInformation": "Thanks for using our service",
            "notes": "Test information",
            "factoringText": "string",
            "number": f"55958-{company_id}", 
            "agreementNumber": f"FIN072024-{company_id}", 
            "version": "2024-07-30T15:04:58.970Z"
        }


        # Get company information
        logger.debug(f"Fetching company information for company_id: {company_id}")
        query_glob = CRP.query(f'Comp_No == {company_id}')
        
        if not query_glob.empty:
            company_nbr = query_glob['Comp_No'].iloc[0]
            company_name = query_glob['Comp_Name'].iloc[0]
            company_street = query_glob['Street'].iloc[0]
            company_zipCode = query_glob['ZipCode'].iloc[0]
            company_city = query_glob['City'].iloc[0]
            company_phone = query_glob['Phone'].iloc[0]

            # Set company information in invoice data
            invoice_data["counterParty"] = {
                "identifier": str(company_nbr),
                "customerNumber": str(company_phone),
                "email": "test@mail.com",
                "counterPartyAddress": {
                    "name": str(company_name),
                    "street": str(company_street),
                    "zip": str(company_zipCode),
                    "city": str(company_city),
                }
            }
            invoice_data["billingAddress"] = {
                "name": str(company_name),
                "street": str(company_street),
                "zip": str(company_zipCode),
                "city": str(company_city),
            }
        else:
            logger.error(f"No data found for company_id: {company_id}")
            continue

        # Process each EPAN for this company
        for epan in epans:
            ticket_epan = TicketEpan(epan)
            
            ptct_id = int(ticket_epan.ptcpid)
            type_id = int(ticket_epan.season_parker)
            
            filtered_df = PPA[PPA['TicketEPAN'] == epan]
            if filtered_df.empty:
                logger.warning(f"No data found for EPAN: {epan}")
                continue
            
            # Aggregate data for the entire month
            sum_Quantity = filtered_df['Quantity'].sum()
            Discount = filtered_df['Discounted']
            Price = filtered_df['Price'].mean()
            Turnover = filtered_df['Turnover'].sum()
            NetPrice = filtered_df['NetPrice'].sum()
            
            query = CRP.query(f'Comp_No == {company_id} & PTCPT_No == {ptct_id}')
            if not query.empty:
                participant_lname = query['PTCPT_Surname'].iloc[0]
                company_startDate = query['PTCPT_ContractStart'].iloc[0]
                company_endDate = query['PTCPT_ContractEnd'].iloc[0]

                discount_Val = calculate_discount_percentage(Price, Turnover)
                
                invoice_row = {
                    "product": str(participant_lname),
                    "productCode": str(type_id),
                    "quantity": float(sum_Quantity),
                    "unit": "NO_UNIT",
                    "unitPrice": float(Price),
                    "discountPercent": max(0, float(discount_Val)),
                    "vatPercent": 14,
                    "startDate": date_format(company_startDate),
                    "endDate": date_format(company_endDate)
                }
                invoice_data["invoiceRows"].append(invoice_row)
            else:
                logger.warning(f"No data found for ptct_id: {ptct_id} in company_id: {company_id}")
                continue

        # Create invoice for this company
        logger.debug(f"Creating invoice for company {company_id}")
        logger.info(invoice_data)
        response = create_invoices(invoice_data)
        if response:
            logger.info(f"Invoice created for company {company_id}. Response: {response}")
        else:
            logger.error(f"Failed to create invoice for company {company_id}")

        logger.info("Monthly invoicing process completed . . . . . . . . . . . . . . . . . . . .")