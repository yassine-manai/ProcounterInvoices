from typing import Dict, Any
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from config.config import BEARER_TOKEN
from config.log_config import logger

def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

class ProcountorAPIError(Exception):
    message: str = ""
    status_code: int = None
    response_content: Any = None

def make_request(method: str, url: str, **kwargs) -> requests.Response:
    headers = get_headers()
    logger.debug(f"Making {method} request to {url} with headers: {headers}")
    
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        
        logger.debug(f"Received response [{response.status_code}] from {url}")
        return response

    except HTTPError as http_err:
        error = ProcountorAPIError(f"HTTP error occurred: {http_err}")
        error.status_code = response.status_code
        error.response_content = response.text
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