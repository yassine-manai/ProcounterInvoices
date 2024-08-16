""" import requests
from typing import Any, Dict, List, Optional, Union
from config.config import BEARER_TOKEN, PROCOUNTOR_URL
from procountor.enum.short_Enum import DocumentInvoiceType
from procountor.models.invoice_model import CommentDTO, CommentEvent, Invoice, MarkInvoiceAsPaid
from config.log_config import logger

# Assuming you have the bearer token
def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }


def request_meth(method: str, url: str, **kwargs) -> requests.Response:
    headers = get_headers()
    logger.debug(f"Making {method} request to {url} with headers: {headers}")
    
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        logger.debug(f"Received response [{response.status_code}] from {url}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise
    


def search_invoices(params: Dict[str, Any] = None) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices"
    headers = get_headers()
    
    logger.debug(f"Making GET request to {url} with headers: {headers}")

    response = requests.get(url, params=params, headers=headers)
    return response

def create_invoice(data: Invoice) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices"
    headers = get_headers()
    response = requests.post(url, json=data.dict(), headers=headers)
    return response

def get_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}"
    headers = get_headers()
    
    logger.debug(f"Making GET request to {url} with headers: {headers}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        
        logger.debug(f"Received response [{response.status_code}] from {url}")
        return response
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise 

def update_invoice(invoice_id: int, data: Invoice) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}"
    headers = get_headers()
    response = requests.put(url, json=data.dict(), headers=headers)
    return response

def approve_invoice(invoice_id: int, comment: str = "") -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/approve"
    headers = get_headers()
    data = {
        "comment": comment[:100]
    }
    response = requests.put(url, json=data, headers=headers)
    return response


def get_invoice_comments(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response


def add_invoice_comment(invoice_id: int, data: CommentDTO) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments"
    headers = get_headers()
    response = requests.post(url, json=data, headers=headers)
    return response 


def get_taggable_users(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments/taggableusers"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response


def get_invoice_image(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/image"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response


def invalidate_invoice(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/invalidate"
    headers = get_headers()
    response = requests.put(url, headers=headers)
    return response

def update_invoice_notes(invoice_id: int, notes: str) -> requests.Response:
    if not (0 <= len(notes) <= 10000):
        raise ValueError("Notes must be between 0 and 10,000 characters.")
    
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/notes"
    headers = get_headers()
    data = {"notes": notes}
    response = requests.put(url, json=data, headers=headers)
    return response

def get_payment_events(invoice_id: str, previous_id: Optional[int] = None, order_by_id: str = "DESC", size: int = 50, page: int = 0) -> requests.Response:
    if size > 200:
        raise ValueError("Page size cannot exceed 200.")
    
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents"
    headers = get_headers()
    params: Dict[str, Any] = {
        "orderById": order_by_id,
        "size": size,
        "page": page
    }
    
    if previous_id is not None:
        params["previousId"] = previous_id
    
    response = requests.get(url, headers=headers, params=params)
    return response


def get_payment_event(invoice_id: int, payment_event_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/{payment_event_id}"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response

def remove_payment_event(invoice_id: int, payment_event_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/{payment_event_id}"
    headers = get_headers()
    response = requests.delete(url, headers=headers)
    return response

def mark_invoice_paid(invoice_id: int, data: MarkInvoiceAsPaid) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/markpaid"
    headers = get_headers()
    response = requests.put(url, headers=headers, json=data.dict())
    return response

def reject_invoice(invoice_id: int, data: dict) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/reject"
    headers = get_headers()
    
    response = requests.put(url, headers=headers, json=data)
    return response


def send_invoice(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/send"
    headers = get_headers()
    response = requests.put(url, headers=headers)
    return response

def send_invoice_to_circulation(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/sendToCirculation"
    headers = get_headers()
    response = requests.put(url, headers=headers)
    return response

def get_invoice_transactions(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/transactions"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response

def set_invoice_unfinished(invoice_id: int) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/unfinished"
    headers = get_headers()
    response = requests.put(url, headers=headers)
    return response

def verify_invoice(invoice_id: int, data: CommentEvent) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/verify"
    headers = get_headers()
    response = requests.put(url, headers=headers, json=data.dict())
    return response


def confirm_action(transaction_identifier: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{transaction_identifier}/confirm"
    headers = get_headers()
    response = requests.put(url, headers=headers)
    return response

def get_personal_approvals(invoice_type: Optional[DocumentInvoiceType] = None) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/personalapprovals"
    headers = get_headers()
    
    # Add query parameters if invoice_type is provided
    params = {}
    if invoice_type:
        params['type'] = invoice_type.value

    response = requests.get(url, headers=headers, params=params)
    return response


def get_personal_verifications(invoice_type: Optional[DocumentInvoiceType] = None) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/personalverifications"
    headers = get_headers()
    params = {}
    if invoice_type:
        params['type'] = invoice_type.value

    response = requests.get(url, headers=headers, params=params)    
    return response
 """