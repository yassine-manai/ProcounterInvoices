from classes.ticket_epan import TicketEpan
from config.config import ACCOUNT_NUMBER, BIC
from config.log_config import logger
from functions.data_format import date_format
from functions.discount_fn import calculate_discount_percentage
from procountor.api.invoicePost import create_invoices
from collections import defaultdict


def flatFee_c1_cp(date_str,PPA,CRP,STR):


    # Process PPA tickets
    epanlist = STR.TicketEPAN.unique()
    logger.debug(f"\n Unique EPANs found: {len(epanlist)} \n")

    company_epans = defaultdict(list)
    for epan in epanlist:
        ticket_epan = TicketEpan(epan)
        company_epans[int(ticket_epan.company_id)].append(epan)


    # Create invoices
    for company_id, epans in company_epans.items():
        company_id = int(company_id)  
        
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
        query_glob = CRP.query(f'Comp_No == {int(company_id)}')

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
            
            sum_Quantity = filtered_df['Quantity'].sum()
            Discount = filtered_df['Discounted'].iloc[0]
            Price = filtered_df['Price'].iloc[0]
            Turnover = filtered_df['Turnover'].iloc[0]
            NetPrice = filtered_df['NetPrice'].iloc[0]
            
            query = CRP.query(f'Comp_No == {int(company_id)} & PTCPT_No == {ptct_id}')

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
                    "discountPercent": float(discount_Val),
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
        response = create_invoices(invoice_data)
        if response:
            logger.info(f"Invoice created for company {company_id}. Response: {response}")
        else:
            logger.error(f"Failed to create invoice for company {company_id}")










