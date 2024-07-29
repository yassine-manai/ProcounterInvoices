from typing import Dict
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from Models.model import ProcountorAPIError
from config.log_config import logger
from globalvars.glob_data import token_data


def get_headers() -> Dict[str, str]:
    global token_data
    token = token_data.get("access_token")

    logger.info(f"Token Fetched. . . ")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def make_request(method: str, url: str, **kwargs) -> dict:
    headers = get_headers()
    logger.debug(f"Making {method} request to {url} with headers: {headers}")
    
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        
        logger.debug(f"Received response [{response.status_code}] from {url}")
        return response.json()  # Return the response content as a dictionary

    except HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err}"
        response_content = getattr(http_err.response, 'text', str(http_err))
        status_code = getattr(http_err.response, 'status_code', 'Unknown')

        error = ProcountorAPIError(error_message)
        error.status_code = status_code
        error.response_content = response_content
        logger.error(error.message)
        raise error

    except ConnectionError as conn_err:
        error = ProcountorAPIError(f"Connection error occurred: {conn_err}")
        logger.error(error.message)
        raise error

    except Timeout as timeout_err:
        error = ProcountorAPIError(f"Timeout error occurred: {timeout_err}")
        logger.error(error.message)
        raise error

    except RequestException as req_err:
        error = ProcountorAPIError(f"An error occurred while making the request: {req_err}")
        logger.error(error.message)
        raise error

    except Exception as e:
        error = ProcountorAPIError(f"An unexpected error occurred: {e}")
        logger.error(error.message)
        raise error