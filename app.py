from collections import defaultdict
from datetime import datetime
import time
from classes.ticket_epan import TicketEpan
from config.config import FILES_PATH
from config.log_config import logger
from functions.read_psv_files import read_file
from dateutil.parser import parse
import pandas as pd 



# Start Execution
logger.info("Starting Process . . . . . . . . . . . . . . . . . . . . .") 

# Get current date
date_str = datetime.now().strftime("%Y-%m-%d")
# Get LastMonth
cur_month = time.strftime("%m")
lst_month = f"0{str(int(time.strftime("%m"))-1 )}"
cur_Year = time.strftime("%Y")

current_date = datetime.now()
current_year = current_date.year
last_month = current_date.month - 1 if current_date.month > 1 else 12
last_month_year = current_year if current_date.month > 1 else current_year - 1

print(current_date)
print(current_year)
print(f"0{last_month}")
print(last_month_year)


logger.debug(f"Current date: {date_str} --------------- Current month: {cur_month} --------  last_month: {lst_month} ------------ Current year: {cur_Year}")
print("\n")

# Define file paths
ppa_file_path = f"{FILES_PATH}/PPA-240528.PSV"
crp_file_path = f"{FILES_PATH}/CRP-240528.PSV"
#str_file_path = "./DEP/STR-240606.PSV"
ppa_c2 = f"./DEP/PPA-*.PSV"
crp_c2= f"./DEP/CRP-*.PSV"



# Read data from files 
logger.debug(f"Reading PPA file from {ppa_file_path}")
PPA = read_file(ppa_file_path)
logger.debug(f"Reading CRP file from {crp_file_path}")
CRP = read_file(crp_file_path)



if PPA.empty and CRP.empty:
    print("PPA file is empty . . . ")
    pass

if CRP.empty:
    print("CRP file is empty . . . ")
    pass
    

# CRP FILE PROCESSING
if not CRP.empty:
    print("\n")
    logger.debug(f" ------------------------- Company's Name------------------------- ")
    Company_ids = set()
    Company_ids.update(CRP["Comp_No"].values.tolist())
    comp_ids_List = list(Company_ids)
    logger.debug(comp_ids_List)
    
    print("\n")
    logger.debug(f" ------------------------- Company's ID------------------------- ")
    Company_names = set()
    Company_names.update(CRP["Comp_Name"].values.tolist())
    comp_names_List = list(Company_names)
    logger.debug(comp_names_List)


    
    
    print("\n")    
    logger.debug(f" ------------------------- Company's DATA ------------------------- ")
    company_data_list = []

    for company_id in comp_ids_List:
        query_data = CRP.query(f'Comp_No == {int(company_id)}')
        
        if not query_data.empty:

            company_info = {
                'Comp_No': int(query_data['Comp_No'].iloc[0]),
                'Comp_Name': query_data['Comp_Name'].iloc[0],
                'Street': query_data['Street'].iloc[0] if not pd.isna(query_data['Street'].iloc[0]) else '',
                'ZipCode': int(query_data['ZipCode'].iloc[0]) if not pd.isna(query_data['ZipCode'].iloc[0]) else 0,
                'City': query_data['City'].iloc[0] if not pd.isna(query_data['City'].iloc[0]) else '',
                'Phone': query_data['Phone'].iloc[0] if not pd.isna(query_data['Phone'].iloc[0]) else '',
                'Comp_MonthLumpSum': int(query_data['Comp_MonthLumpSum'].iloc[0]) if not pd.isna(query_data['Comp_MonthLumpSum'].iloc[0]) else 0,
                'Comp_ContractStart': query_data['Comp_ContractStart'].iloc[0] if not pd.isna(query_data['Comp_ContractStart'].iloc[0]) else '',
                'Comp_ContractEnd': query_data['Comp_ContractEnd'].iloc[0] if not pd.isna(query_data['Comp_ContractEnd'].iloc[0]) else '',
            }
            
            # Convert to datetime if not None
            if company_info['Comp_ContractStart']:
                try:
                    company_info['Comp_ContractStart'] = parse(company_info['Comp_ContractStart'])
                except (ValueError, TypeError):
                    company_info['Comp_ContractStart'] = None
            
            if company_info['Comp_ContractEnd']:
                try:
                    company_info['Comp_ContractEnd'] = parse(company_info['Comp_ContractEnd'])
                except (ValueError, TypeError):
                    company_info['Comp_ContractEnd'] = None
            
            
            company_data_list.append(company_info)
            
    logger.debug(company_data_list)
    logger.debug(len(company_data_list))
    
        
    
    print("\n")
    logger.debug(f" ------------------------- Valid Company's DATA ------------------------- ")
    valid_company_data_list = []
    
    # Get the current date
    current_date = datetime.now()

    if current_date.month == 1:
        last_month = 12
        last_month_year = current_date.year - 1
    else:
        last_month = current_date.month - 1
        last_month_year = current_date.year

    for company_info in company_data_list:
        contract_end_date = company_info.get('Comp_ContractEnd')
        
        if contract_end_date:
            if not (contract_end_date.month == last_month and contract_end_date.year == last_month_year) and contract_end_date > current_date:
                valid_company_data_list.append(company_info)

    logger.debug(valid_company_data_list)
    logger.debug(len(valid_company_data_list))

    print("\n")
    logger.debug(f" ------------------------- CHECK LUM SUM ------------------------- ")
    Lum_Sum_list = []
    
    for company in valid_company_data_list:
        lum_sum = company.get('Comp_MonthLumpSum')
        company_id = company.get('Comp_No')
        
        if lum_sum == 0:
            #logger.debug(f"Comp_MonthLumpSum is 0 for company {company_id}")
            continue 
        
        if lum_sum != 0:
            #logger.debug(f"Comp_MonthLumpSum is {lum_sum} for company {company_id}")
            Lum_Sum_list.append({
                'Comp_No': company_id,
                'Comp_MonthLumpSum': lum_sum
            })

    
    logger.debug(Lum_Sum_list)
    
    
    logger.debug(f" ------------------------- CHECK Company Name with name ------------------------- ")
    

    
    
    
    
    
    
    
"""     query_company = CRP.query('Comp_No')
    query_name = CRP.query('Comp_Name')
    
    for company in query_company:
        print(query_company)
        
        company_nbr = query_company['Comp_No'].iloc[0]
        company_name = query_company['Comp_Name'].iloc[0]
        company_street = query_company['Street'].iloc[0]
        company_zipCode = query_company['ZipCode'].iloc[0]
        company_city = query_company['City'].iloc[0]
        company_phone = query_company['Phone'].iloc[0]
        company_monthLumSum = query_company['Comp_MonthLumpSum'].iloc[0]
        company_ContractStart = query_company['Comp_ContractStart'].iloc[0]
        company_ContractEnd = query_company['Comp_ContractEnd'].iloc[0]

        logger.info(f"{company_nbr} ---- {company_name} ----{company_monthLumSum} ----{company_ContractStart} ---- {company_ContractEnd}")
        print("\n")
        
        
        logger.debug(f" ------------------------- Check Company DATE Validity ------------------------- ")
        contract_end_date = datetime.strptime(company_ContractEnd, "%d.%m.%Y")
        contract_end_month = contract_end_date.month
        contract_end_year = contract_end_date.year
        
        
        if contract_end_month == last_month and contract_end_year == last_month_year:
            print("The contract end date is in the last month of the current year.")
        else:
            print("The contract end date is not in the last month of the current year.")
         """
        
    


    




# PPA FILE PROCESSING
""" if not PPA.empty:
    epanlist = PPA.TicketEPAN.unique()
    logger.debug(f" ------------------------- Unique EPANs found: {len(epanlist)} ------------------------- ") 
    logger.debug(f"\n List : {epanlist} ")
     """