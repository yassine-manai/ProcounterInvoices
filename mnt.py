from collections import defaultdict
from datetime import datetime
from classes.ticket_epan import TicketEpan
from config.config import ACCOUNT_NUMBER, BIC
from config.log_config import logger
from functions.data_format import date_format
from functions.discount_fn import calculate_discount_percentage
from functions.extract_month_file import find_files_last_month
import pandas as pd
from functions.read_psv_files import read_file
from procountor.api.invoicePost import create_invoices

def mnt():
    directory = './DEP'
    files_PPA = find_files_last_month(directory, 'PPA')
    files_CRP = find_files_last_month(directory, 'CRP')
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Log file existence
    if files_CRP:
        logger.success(f"Files found in last month: {len(files_CRP)} with type CRP")
    else:
        logger.error("Files (CRP) not found for last month ")

    if files_PPA:
        logger.success(f"Files found in last month: {len(files_PPA)} with type PPA")
    else:
        logger.error("Files (PPA) not found for last month ")

    # DATAFRAMES
    CRP_DF = pd.DataFrame()
    PPA_DF = pd.DataFrame()

    logger.info("Reading CRP files")
    for file in files_CRP:
        actualdf = read_file(file)
        CRP_DF = pd.concat([CRP_DF, actualdf], ignore_index=True)

    columns_to_drop = [
        'TradingDate', 'PtcFree1', 'PtcFree2', 'PtcFree3', 'CompFree1', 'CompFree2', 'CompFree3', 'WeekProfile',
        'Comp_ShortName', 'Telefax', 'InvoicingGroup', 'Status', 'Deposit', 'Bank', 'BankCode', 'AccountNo',
        'PTCPT_Remove', 'PTCPT_Blocked', 'Matchcode', 'ProdTime', 'ParkSpaceNo', 'PTCPT_Limit',
        'Admission', 'Calculation', 'OverDraft', 'Balance', 'Telefax'
    ]

    CRP_DF = CRP_DF.drop(columns=columns_to_drop)
    CRP_DF = CRP_DF.drop_duplicates().sort_values(by='Comp_No').reset_index(drop=True)

    # Convert contract start and end dates to datetime
    CRP_DF['PTCPT_ContractStart'] = pd.to_datetime(CRP_DF['PTCPT_ContractStart'], format='%d.%m.%Y')
    CRP_DF['PTCPT_ContractEnd'] = pd.to_datetime(CRP_DF['PTCPT_ContractEnd'], format='%d.%m.%Y')

    start_date = '2024-07-01'
    end_date = '2024-07-30'

    # Filter by current date range --> for epans
    filtered_df_range = CRP_DF[(CRP_DF['PTCPT_ContractStart'] < end_date) & (CRP_DF['PTCPT_ContractEnd'] > start_date)]

    # Filter by MonthSum for both Ptcpt and company --> for monthly sum
    month_df_filter = filtered_df_range[(filtered_df_range['PTCPT_MonthLumpSum'] > 0) | (filtered_df_range['Comp_MonthLumpSum'] > 0)]

    # Create a dictionary of company names and their associated IDs
    Company_names_list = set(filtered_df_range["Comp_Name"].values.tolist())
    company_ids_dict = {company_name: set(filtered_df_range.query(f'Comp_Name == "{company_name}"')['Comp_No'].values.tolist())
                        for company_name in Company_names_list}

    logger.info("Reading PPA files")
    for file in files_PPA:
        actual_ppa_df = read_file(file)
        PPA_DF = pd.concat([PPA_DF, actual_ppa_df], ignore_index=True)

    columns_to_drop_ppa = [
        'TradingDate', 'SiteCarParkNumber', 'CellComputerNo', 'PaymentNumber', 'DeviceNumber', 'PaymentType',
        'PaymentMethod', 'ShiftID', 'PaymentReason', 'PaymentCount', 'Cashier', 'ReceiptNo', 'TariffKey', 'FirstPaymntNo'
    ]
    PPA_DF = PPA_DF.drop(columns=columns_to_drop_ppa)

    epanlist = PPA_DF.TicketEPAN.unique()
    logger.debug(len(epanlist))
    logger.debug(epanlist)

    # Extract Company ID with EPANs number
    company_epans = defaultdict(list)
    for epan in epanlist:
        ticket_epan = TicketEpan(epan)
        company_epans[int(ticket_epan.company_id)].append(epan)
    logger.info(company_epans)

    # Iterate over companies to create invoices
    for company_name in Company_names_list:
        logger.info(f"Processing company: {company_name}")

        query_PPA = filtered_df_range.query(f'Comp_Name == "{company_name}"')
        if query_PPA.empty:
            logger.warning(f"No data found for company name: {company_name}")
            continue

        company_id = query_PPA['Comp_No'].iloc[0]
        invoice_data = None

        # Monthly Sum data
        query_month = month_df_filter.query(f'Comp_Name == "{company_name}"')
        if not query_month.empty:
            company_id_month = query_month['Comp_No'].iloc[0]
            company_nbr = query_month['Comp_No'].iloc[0]
            company_name = query_month['Comp_Name'].iloc[0]
            company_street = query_month['Street'].iloc[0]
            company_zipCode = query_month['ZipCode'].iloc[0]
            company_city = query_month['City'].iloc[0]
            company_phone = query_month['Phone'].iloc[0]
            company_ContractStart = query_month['Comp_ContractStart'].iloc[0]
            company_ContractEnd = query_month['Comp_ContractEnd'].iloc[0]

            invoice_data = {
                "type": "SALES_INVOICE",
                "status": "UNFINISHED",
                "date": str(date_str),
                "counterParty": {
                    "identifier": str(company_nbr),
                    "customerNumber": str(company_phone),
                    "email": "test@mail.com",
                    "counterPartyAddress": {
                        "name": str(company_name),
                        "street": str(company_street),
                        "zip": str(company_zipCode),
                        "city": str(company_city),
                    }
                },
                "billingAddress": {
                    "name": str(company_name),
                    "street": str(company_street),
                    "zip": str(company_zipCode),
                    "city": str(company_city),
                },
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
                "number": f"2024-{company_id_month}",
                "agreementNumber": f"FIN-{company_id_month}",
                "version": "2024-07-30T15:04:58.970Z"
            }

            # Process Monthly Lump Sum Data
            for ptct_id in company_ids_dict[company_name]:
                query = filtered_df_range.query(f'Comp_No == {company_id} & PTCPT_No == {ptct_id}')
                if query.empty:
                    logger.warning(f"No matching participant data found for company_name: {company_name}, ptct_id: {ptct_id}")
                    continue

                participant_lname = query['PTCPT_Surname'].iloc[0]
                participant_endDate = query['PTCPT_ContractEnd'].iloc[0]
                participant_MonthLumpSum = query['PTCPT_MonthLumpSum'].iloc[0]

                discount_Val = calculate_discount_percentage(participant_MonthLumpSum, participant_MonthLumpSum)

                invoice_row = {
                    "product": str(participant_lname),
                    "productCode": str(ptct_id),
                    "quantity": 1,
                    "unit": "NO_UNIT",
                    "unitPrice": float(participant_MonthLumpSum),
                    "discountPercent": float(discount_Val),
                    "netAmount": float(participant_MonthLumpSum),
                    "vatPercent": 14,
                    "vatAmount": participant_MonthLumpSum * 0.14,
                    "totalAmount": float(participant_MonthLumpSum * 1.14),
                    "description": f"Monthly lump sum for {participant_lname} until {participant_endDate}",
                }
                invoice_data["invoiceRows"].append(invoice_row)
                logger.success(f"Invoice row added for participant: {participant_lname}")

            # Process PPA Data
            if company_id in company_epans:
                for epan in company_epans[company_id]:
                    ticket_epan = TicketEpan(epan)
                    ptct_id = int(ticket_epan.ptcpid)
                    type_id = int(ticket_epan.type_parker)

                    filtered_df = PPA_DF[PPA_DF['TicketEPAN'] == epan]
                    if filtered_df.empty:
                        logger.warning(f"No data found for EPAN: {epan}")
                        continue

                    sum_Quantity = filtered_df['Quantity'].sum()
                    Price = filtered_df['Price'].iloc[0]
                    Turnover = filtered_df['Turnover'].iloc[0]
                    NetPrice = filtered_df['NetPrice'].iloc[0]

                    query = filtered_df_range.query(f'Comp_No == {company_id} & PTCPT_No == {ptct_id}')
                    if query.empty:
                        logger.warning(f"No matching participant data found for EPAN: {epan}")
                        continue

                    participant_lname = query['PTCPT_Surname'].iloc[0]
                    participant_endDate = query['PTCPT_ContractEnd'].iloc[0]

                    discount_Val = calculate_discount_percentage(Price, Turnover)

                    invoice_row = {
                        "product": str(participant_lname),
                        "productCode": str(type_id),
                        "quantity": float(sum_Quantity),
                        "unit": "NO_UNIT",
                        "unitPrice": float(Price),
                        "discountPercent": float(discount_Val),
                        "netAmount": float(NetPrice),
                        "vatPercent": 24,
                        "vatAmount": NetPrice * 0.24,
                        "totalAmount": float(Turnover),
                        "description": f"All costs regarding {participant_lname} until {participant_endDate}",
                    }
                    invoice_data["invoiceRows"].append(invoice_row)
                    logger.success(f"Invoice row added for EPAN: {epan}")
            else:
                logger.error(f"No matching company data found for company: {company_name}")

        if invoice_data and invoice_data["invoiceRows"]:
            # Create invoice for this company
            logger.debug(f"Creating invoice for company {company_id}")
            response = create_invoices(invoice_data)
            if response:
                logger.info(f"Invoice created for company {company_id}. Response: {response}")
            else:
                logger.error(f"Failed to create invoice for company {company_id}")
        else:
            logger.error(f"No invoice rows were generated; cannot send request for company: {company_name}")


#filtered_df_range.to_csv("testt.csv", index=False)



