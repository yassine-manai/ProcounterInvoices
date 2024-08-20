from classes.ticket_epan import TicketEpan
from config.config import ACCOUNT_NUMBER, BIC
from config.log_config import logger
from functions.data_format import date_format
from functions.discount_fn import calculate_discount_percentage
from procountor.api.invoicePost import create_invoices
from collections import defaultdict
from dateutil.parser import parse


def flatFee_c1(date_str,PPA,CRP):

    """
        Processes ticket data and creates invoices for each company.

        This function performs the following tasks:
        1. Processes unique TicketEPAN values from the given DataFrame `PPA` to group tickets by company.
        2. For each company, creates an invoice with appropriate details including company information and invoice rows.
        3. Fetches company information from the `CRP` DataFrame and populates the invoice with relevant details.
        4. Calculates discount percentages and prepares invoice rows based on the ticket data.
        5. Calls an external API to create invoices for each company.

        Parameters:
            date_str (str): The date string to be used in the invoice.
            PPA (pd.DataFrame): DataFrame containing ticket information with columns including 'TicketEPAN', 'Quantity', 'Discounted', 'Price', 'Turnover', and 'NetPrice'.
            CRP (pd.DataFrame): DataFrame containing company and participant information with columns including 'Comp_No', 'Comp_Name', 'Street', 'ZipCode', 'City', 'Phone', 'PTCPT_Surname', 'PTCPT_ContractStart', 'PTCPT_ContractEnd', and 'PTCPT_No'.

        Returns:
            None

        Raises:
            ValueError: If any required data is missing or improperly formatted.
    """
    
    if PPA.empty and CRP.empty:
        print("Files is empty . . . ")
        pass
    
    if not PPA.empty and not CRP.empty:
        # Process PPA tickets
        epanlist = PPA.TicketEPAN.unique()
        logger.debug(f" ------------------------- Unique EPANs found: {len(epanlist)} ------------------------- ") 
        logger.debug(f"\n List : {epanlist} -------------------------")

         
        # Extract Company ID with EPANS number
        company_epans = defaultdict(list)
        for epan in epanlist:
            ticket_epan = TicketEpan(epan)
            company_epans[int(ticket_epan.company_id)].append(epan)
            
        logger.debug(f" ------------------------- company EPAN found------------------------- ")
        logger.info(company_epans)
        
        
        

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
                "number": f"2024-{company_id}", 
                "agreementNumber": f"FIN072024-{company_id}", 
                "version": "2024-07-30T15:04:58.970Z"
            }

            # Get company information
            logger.debug(f"Fetching company information for company_id: {company_id}")
            query_glob = CRP.query(f'Comp_No == {int(company_id)}')
            #query_name = CRP.query(f'Comp_Name == {int(company_id)}')

           
            if not query_glob.empty:
                company_nbr = query_glob['Comp_No'].iloc[0]
                company_name = query_glob['Comp_Name'].iloc[0]
                company_street = query_glob['Street'].iloc[0]
                company_zipCode = query_glob['ZipCode'].iloc[0]
                company_city = query_glob['City'].iloc[0]
                company_phone = query_glob['Phone'].iloc[0]
                company_monthLumSum = query_glob['Comp_MonthLumpSum'].iloc[0]
                company_ContractStart = parse(query_glob['Comp_ContractStart'].iloc[0])
                company_ContractEnd = parse(query_glob['Comp_ContractEnd'].iloc[0])

                
                if company_monthLumSum == 0:
                    pass
                            
                if company_monthLumSum != 0 : 
                    cmp_monthLumSum = company_monthLumSum
                    logger.debug(f"{company_monthLumSum} -------- {company_id} ---------- {cmp_monthLumSum} -------- {company_name}")
                
                    

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

            # Process each EPAN for x company
            for epan in epans:
                ticket_epan = TicketEpan(epan)
                
                ptct_id = int(ticket_epan.ptcpid)
                type_id = int(ticket_epan.type_parker)
                
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
                    participant_startDate = parse(query['PTCPT_ContractStart'].iloc[0])
                    participant_endDate = parse(query['PTCPT_ContractEnd'].iloc[0])
                    participant_MonthLumpSum = query['PTCPT_MonthLumpSum'].iloc[0]
                    print(f"{participant_endDate} ---------- {participant_startDate}")
                    print(f"{company_ContractEnd} ---------- {company_ContractStart}")

                    if participant_endDate < company_ContractEnd:
                        #discount_Val = calculate_discount_percentage(Price, Turnover)
                        
                        invoice_row = {
                            "product": str(participant_lname),
                            "productCode": str(type_id),
                            "quantity": float(sum_Quantity),
                            "unit": "NO_UNIT",
                            "unitPrice": float(Price),
                            "discountPercent": float(10),
                            "vatPercent": 14,
                            "startDate": date_format(participant_startDate),
                            "endDate": date_format(participant_endDate)
                        }
                        invoice_data["invoiceRows"].append(invoice_row)
                    else:
                        logger.debug(f"Participant ID {ptct_id} End Date is Expired")
                        pass
                        
                else:
                    logger.warning(f"No data found for Participant_id: {ptct_id} in company_id: {company_id}")
                    continue

            # Create invoice for this company
            logger.debug(f"Creating invoice for company {company_id}")
    """         response = create_invoices(invoice_data)
            if response:
                logger.info(f"Invoice created for company {company_id}. Response: {response}")
            else:
                logger.error(f"Failed to create invoice for company {company_id}")
    """









