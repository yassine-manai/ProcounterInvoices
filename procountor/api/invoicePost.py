import requests
from config.check_error import handle_api_error
from config.config import PROCOUNTOR_URL
from functions.request_api import make_request
from procountor.models.invoice_model import CommentDTO, Invoice


@handle_api_error
def create_invoice(data: Invoice) -> requests.Response:
    return make_request("POST", f"{PROCOUNTOR_URL}/invoices", json=data.dict())

@handle_api_error
def add_invoice_comment(invoice_id: int, data: CommentDTO) -> requests.Response:
    return make_request("POST", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments", json=data)