import time
from config.config import FILES_PATH
from config.log_config import logger
from datetime import datetime
from functions.extract_month_file import find_files_last_month
from invoices.FlatFees.flat_fees_c1 import flatFee_c1
from invoices.FlatFees.flat_Fees_c2 import flatFee_c2
from invoices.FlatFees_copy.flat_fees_c1_cp import flatFee_c1_cp
from invoices.FlatFees_copy.flat_Fees_c2_cp import flatFee_c2_cp
from functions.read_psv_files import read_file, read_psv_from_folder
from functions.animation import animate
from functions.fetch_token import fetch_data_token 
from functions.img_invoices import fetch_invoices_and_images
from classes.ticket_epan import TicketEpan
from mnt import mnt

# Start Execution
logger.info("Starting Process . . . . . . . . . . . . . . . . . . . . .") 

# Get current date
date_str = datetime.now().strftime("%Y-%m-%d")
# Get LastMonth
cur_month = time.strftime("%m")
last_month = f"0{str(int(time.strftime("%m"))-1 )}"


logger.debug(f"Current date: {date_str} + Current month: {cur_month} + last_month: {last_month}")


# Extract Files of last month from folder
""" directory = './DEP'
files_PPA = find_files_last_month(directory,'PPA')
files_CRC = find_files_last_month(directory,'CRC')
 """
""" 
if files_PPA: 
    logger.success(f"Files found in last month: {len(files_PPA)} with type PPA")
    for file in files_PPA:
        logger.info(file)
    
else:
    logger.error(f"Files not found in last month")

print("\n")

if files_CRC: 
    logger.success(f"Files found in last month: {len(files_CRC)} with type CRC")
    for file in files_CRC:
        logger.info(file)
    
else:
    logger.error(f"Files not found in last month ")
 """

""" stepan = read_psv_from_folder("./DEP")
logger.success(f"Files Found :  {len(stepan)}")


for st in stepan:
    if st.TicketEPAN in st and st['TicketEPAN']:
        logger.success(f"EPAN found in {st}")
    else:
        logger.error(f"EPAN not found in {st}")
 """

    
""" if PPA.TicketEPAN:
    logger.success("Ticket EPAN found in PPA file")
    flatFee_c1(date_str,PPA,CRP)
    logger.success("Flat Fee invoice created successfully")
else:
    logger.error("Failed to find TicketEPAN in PPA file")


if STR.TicketEPAN:
    logger.success("Ticket EPAN found in STR file")
    flatFee_c1_cp(date_str,PPA,CRP)
    logger.success("Flat Fee invoice created successfully")
else:
    logger.error("Failed to find TicketEPAN in STR file")
 """

  
# Fetch and log token data
fetch_data_token()
logger.info("Token data fetched and saved")    
 
    
mnt()

""" # create FlatFee invoice for one month --> Case 1
logger.info("Creating FlatFee Monthly invoice . . . ")  
 
if flatFee_c2(date_str,ppa_c2,crp_c2):
    logger.info("Flat Fee Monthly invoice created successfully")
else:
    logger.error("Failed to create Monthly Flat Fee invoice")
 """
    
""" # create FlatFee+overtime invoice --> Case 2
logger.info("Creating FlatFeeOverTime invoice . . . ")  


# create Company pooling invoice --> Case 3
logger.info("Creating Company Pooling invoice . . . ")  
 """


# Get images invoices from the server 
#logger.info("Start Save images Process . . . ")   
#animate()
#fetch_invoices_and_images()
#logger.info("Images Saved Succesfully . . ")    



logger.info("Process completed . . . . . . . . . . . . . . . . . . . .")
