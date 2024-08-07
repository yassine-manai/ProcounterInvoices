from datetime import datetime
from classes.ppd import FilePPD
from classes.ticket_epan import TicketEpan
from config.log_config import logger
from functions.read_psv_files import read_file
from functions.fetch_token import fetch_data_token 
from collections import defaultdict

# Start Execution
logger.info("Starting Process . . . . . . . . . . . . . . . . . . . . .") 

# Get current date
date_str = datetime.now().strftime("%Y-%m-%d")
logger.debug(f"Current date: {date_str}")

# Define file paths
ppa_file_path = "./DEP/PPA-240604.PSV"
crp_file_path = "./DEP/CRP-240604.PSV"
ppd_file_path = "./DEP/PPD-240604.PSV"


# Read data from files
logger.debug(f"Reading PPA file from {ppa_file_path}")
PPA = read_file(ppa_file_path)

logger.debug(f"Reading CRP file from {crp_file_path}")
CRP = read_file(crp_file_path)

logger.debug(f"Reading PPD file from {ppd_file_path}")
PPD = read_file(ppd_file_path)


file_ppd = FilePPD(PPD)
ppd_list = file_ppd.rslts()

#for item in ppd_list:
logger.info("Data ml PPD file ")
logger.info(ppd_list[1])

# Fetch and log token data
#fetch_data_token()
#logger.info("Token data fetched and saved")    

# Process PPA tickets
epans = PPD.TicketEPAN.unique()
logger.debug(f"Unique EPANs found: {len(epans)}  \n {epans}")

for epan in epans:
    ticket_epan = TicketEpan(epan)
    cmp_id = ticket_epan.company_id
    ptct_id = ticket_epan.ptcpid
    logger.debug(f"EPAN: {epan}, Company ID: {int(cmp_id)}, PTCP ID: {int(ptct_id)}")

    print("\n")

    query_glob = CRP.query(f'Comp_No == {int(cmp_id)}')
    
    Tarifstart = query_glob['Comp_No'].iloc[0]
    logger.info(Tarifstart)

# Get company information
logger.debug(f"Fetching company information for company_id: {int(cmp_id)}")
query_glob = CRP.query(f'Comp_No == {int(cmp_id)}')

if not query_glob.empty:
    company_nbr = query_glob['Comp_No'].iloc[0]
    company_name = query_glob['Comp_Name'].iloc[0]
    company_street = query_glob['Street'].iloc[0]
    company_zipCode = query_glob['ZipCode'].iloc[0]
    company_city = query_glob['City'].iloc[0]
    company_phone = query_glob['Phone'].iloc[0]
       
    filtered_df = PPA[PPA['TicketEPAN'] == epan]
    sum_Quantity = filtered_df['Quantity'].sum()
    Discount = filtered_df['Discounted'].iloc[0]
    Price = filtered_df['Price'].iloc[0]
    Turnover = filtered_df['Turnover'].iloc[0]
    NetPrice = filtered_df['NetPrice'].iloc[0]
    
    query = CRP.query(f'Comp_No == {int(cmp_id)} & PTCPT_No == {int(ptct_id)}')

    if not query.empty:
        participant_lname = query['PTCPT_Surname'].iloc[0]
        company_startDate = query['PTCPT_ContractStart'].iloc[0]
        company_endDate = query['PTCPT_ContractEnd'].iloc[0]
        logger.debug(f"Participant Name: {participant_lname}")
            




































logger.info("Process completed . . . . . . . . . . . . . . . . . . . .")
