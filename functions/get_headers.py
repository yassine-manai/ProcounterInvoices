from typing import Dict
from globalvars.glob_data import token_data


def get_headers() -> Dict[str, str]:
    """
    Retrieves the headers required for making API requests, including the authorization token.

    This function constructs and returns the headers needed for API requests, including the
    authorization token fetched from the global `token_data` dictionary.

    Returns:
        Dict[str, str]: A dictionary of headers, including the Authorization and Content-Type headers.
    """
    global token_data
    token = token_data.get("access_token")

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }