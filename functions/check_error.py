import requests
from typing import Any, Optional
from config.log_config import logger

class ProcountorError(Exception):
    """
    Custom exception class for handling Procountor API errors.

    Attributes:
        message (str): The error message.
        status_code (Optional[int]): The HTTP status code, if applicable.
        response_content (Any): The content of the response, if applicable.
    """
    def __init__(self, message: str, status_code: Optional[int] = None, response_content: Any = None):
        """
        Constructs all the necessary attributes for the ProcountorError object.

        Parameters:
            message (str): The error message.
            status_code (Optional[int]): The HTTP status code, if applicable.
            response_content (Any): The content of the response, if applicable.
        """
        self.message = message
        self.status_code = status_code
        self.response_content = response_content
        super().__init__(self.message)

def handle_api_error(func):
    """
    Decorator for handling errors in API calls.

    This decorator catches exceptions that occur during the execution of the
    decorated function and raises a ProcountorError with relevant details.

    Parameters:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with error handling.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise ProcountorError(
                f"API request failed: {str(e)}",
                getattr(e.response, 'status_code', None),
                getattr(e.response, 'text', None)
            )
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            raise ProcountorError(f"Invalid input: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ProcountorError(f"Unexpected error: {str(e)}")
    return wrapper
