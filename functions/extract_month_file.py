from datetime import datetime
import os
import time
import glob
from config.log_config import logger

def find_files_last_month(directory, typeFile):
    """
    Finds and returns a list of files from the specified directory that match the pattern for the last month.

    The function determines the current year and month, calculates the previous month, constructs a search pattern
    to match files from the last month in the format "TYPE-YYMM*.PSV", and returns the list of matching files.

    Parameters:
    directory (str): The directory in which to search for files.
    typeFile (str): The type of file to search for (e.g., "CRP").

    Returns:
    list: A list of file paths that match the search pattern for the last month.
    """
    
    # Get the current year and month
    current_year = time.strftime("%y")  
    current_month = int(time.strftime("%m"))
    logger.debug(f"Current Year: {current_year} -- Current Month: {current_month}")

    # Determine the last month and adjust the year if necessary
    if current_month == 1:
        last_month_year = str(int(current_year) - 1).zfill(2)
        last_month = '12'
    else:
        last_month_year = current_year
        last_month = str(current_month - 1).zfill(2)

    search_pattern = os.path.join(directory, f"{typeFile}-{last_month_year}{last_month}*.PSV")
    logger.debug(f"Search pattern: {search_pattern}")

    if not os.path.exists(directory):
        logger.error(f"Directory does not exist: {directory}")
        return []

    matching_files = glob.glob(search_pattern)

    # Normalize file paths to use forward slashes
    matching_files = [os.path.normpath(file).replace("\\", "/") for file in matching_files]
    #logger.debug(f"Matching files: {matching_files}")

    return matching_files


def get_last_month() -> str:
    current_date = datetime.now()
    last_month = current_date.month - 1 if current_date.month > 1 else 12
    return f"{last_month:02d}"