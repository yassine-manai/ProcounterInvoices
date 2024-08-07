from typing import Dict
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from Models.model import ProcountorAPIError
from config.log_config import logger
from functions.get_headers import get_headers



def make_request(method: str, url: str, **kwargs) -> dict:
    """
    Makes an HTTP request to the specified URL and returns the response details.

    This function performs an HTTP request using the specified method and URL, including any
    additional keyword arguments. It logs detailed information about the request and response,
    and handles various types of exceptions, raising a custom `ProcountorAPIError` in case of errors.

    Parameters:
        method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
        url (str): The URL to which the request is made.
        **kwargs: Additional keyword arguments to pass to the `requests.request` method.

    Returns:
        dict: A dictionary containing the response status code, headers, content, and JSON data (if applicable).

    Raises:
        ProcountorAPIError: If an HTTP error, connection error, timeout, or request exception occurs.
    """
    headers = get_headers()
    logger.debug(f"Making {method} request to {url} with headers: {headers}")

    try:
        response = requests.request(method, url, headers=headers, **kwargs)

        # Log the full response
        logger.debug(f"Received response [{response.status_code}] from {url}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        logger.debug(f"Response content: {response.text}")

        response.raise_for_status()

        # Return a dictionary with all response information
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'json': response.json() if response.headers.get('Content-Type', '').startswith('application/json') else None
        }

    except HTTPError as http_err:
        error = ProcountorAPIError(f"HTTP error occurred: {http_err}")
        error.status_code = response.status_code
        error.response_content = response.text
        error.response_headers = dict(response.headers)
        logger.error(f"HTTP Error: {error.message}")
        logger.error(f"Status Code: {error.status_code}")
        logger.error(f"Response Content: {error.response_content}")
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
