import requests
from config.log_config import logger
from globalvars.glob_data import token_data
from config.config import API_KEY, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, PROCOUNTOR_URL_TOKEN


def fetch_data_token():
    global token_data
    url = PROCOUNTOR_URL_TOKEN
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': GRANT_TYPE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'api_key': API_KEY
    }

    try:
        logger.debug(f"Making a POST request . . .")

        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
                        
            data = response.json()
            
            token_data['access_token'] = data.get('access_token',"ABCDEF")
            token_data['token_type'] = data.get('token_type',"Bearer")
            token_data['expires_in'] = data.get('expirers_in',3600)
            
            logger.debug(f" Data fetched : {token_data} with status code: {response.status_code}")

        
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
