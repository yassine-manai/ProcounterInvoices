import requests
from typing import Any, Dict, Optional
from config.check_error import handle_api_error
from config.config import PROCOUNTOR_URL
from functions.request_api import make_request
from procountor.enum.short_Enum import DocumentInvoiceType
from config import *

url_post = "https://pts-procountor.pubdev.azure.procountor.com/api"

@handle_api_error
def search_invoices(params: Dict[str, Any] = None) -> requests.Response:
    return make_request("GET", f"{url_post}/invoices", params=params)

@handle_api_error
def get_invoice(invoice_id: str) -> requests.Response:
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}")

@handle_api_error
def get_all_invoice() -> requests.Response:
    return make_request("GET", f"{url_post}/invoices")

@handle_api_error
def get_invoice_comments(invoice_id: int) -> requests.Response:
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments")

@handle_api_error
def get_taggable_users(invoice_id: int) -> requests.Response:
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments/taggableusers")

@handle_api_error
def get_invoice_image(invoice_id: int) -> requests.Response:
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/image")

@handle_api_error
def get_payment_events(invoice_id: str, previous_id: Optional[int] = None, order_by_id: str = "DESC", size: int = 50, page: int = 0) -> requests.Response:
    if size > 200:
        raise ValueError("Page size cannot exceed 200.")
    
    params: Dict[str, Any] = {
        "orderById": order_by_id,
        "size": size,
        "page": page
    }
    
    if previous_id is not None:
        params["previousId"] = previous_id
    
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents", params=params)

@handle_api_error
def get_payment_event(invoice_id: int, payment_event_id: int) -> requests.Response:
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/{payment_event_id}")

@handle_api_error
def get_invoice_transactions(invoice_id: int) -> requests.Response:
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/transactions")

@handle_api_error
def get_personal_approvals(invoice_type: Optional[DocumentInvoiceType] = None) -> requests.Response:
    params = {}
    if invoice_type:
        params['type'] = invoice_type.value
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/personalapprovals", params=params)

@handle_api_error
def get_personal_verifications(invoice_type: Optional[DocumentInvoiceType] = None) -> requests.Response:
    params = {}
    if invoice_type:
        params['type'] = invoice_type.value
    return make_request("GET", f"{PROCOUNTOR_URL}/invoices/personalverifications", params=params)