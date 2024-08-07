import requests
from functions.check_error import handle_api_error
from config.config import PROCOUNTOR_URL
from functions.request_api import make_request
from functions.get_headers import get_headers
from procountor.models.invoice_model import CommentDTO, Invoice
from config.log_config import logger


#url_post = "https://pts-procountor.pubdev.azure.procountor.com/api/invoices"
url_post = f"{PROCOUNTOR_URL}/invoices"


@handle_api_error
def create_invoices(data: Invoice) -> requests.Response:
    logger.debug(f"\n {url_post}")
    return make_request("POST", url_post, json=data)


@handle_api_error
def add_invoice_comment(invoice_id: int, data: CommentDTO) -> requests.Response:
    return make_request("POST", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments", json=data)


def create_invoiqdssqce(data: Invoice) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices"
    headers = get_headers()
    response = requests.post(url, json=data, headers=headers)
    return response


def create_invoice(invoice_data: Invoice):
    url = f"{PROCOUNTOR_URL}/invoices"
    headers = get_headers()

    
    # Convert the Invoice object to a dictionary
    invoice_dict = invoice_data.model_dump()
    
    # If using an older version of Pydantic, use .dict() instead:
    # invoice_dict = invoice_data.dict(exclude_unset=True)

    try:
        response = requests.post(url, json=invoice_dict, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating invoice: {e}")
        return None