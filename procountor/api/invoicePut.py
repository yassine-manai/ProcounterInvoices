import requests
from typing import Dict
from config.check_error import handle_api_error
from config.config import PROCOUNTOR_URL
from functions.request_api import make_request
from procountor.models.invoice_model import CommentEvent, Invoice, MarkInvoiceAsPaid

@handle_api_error
def update_invoice(invoice_id: int, data: Invoice) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}", json=data.dict())

@handle_api_error
def approve_invoice(invoice_id: int, comment: str = "") -> requests.Response:
    data = {"comment": comment[:100]}
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/approve", json=data)

@handle_api_error
def invalidate_invoice(invoice_id: int) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/invalidate")

@handle_api_error
def update_invoice_notes(invoice_id: int, notes: str) -> requests.Response:
    if not (0 <= len(notes) <= 10000):
        raise ValueError("Notes must be between 0 and 10,000 characters.")
    data = {"notes": notes}
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/notes", json=data)

@handle_api_error
def mark_invoice_paid(invoice_id: int, data: MarkInvoiceAsPaid) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/markpaid", json=data.dict())

@handle_api_error
def reject_invoice(invoice_id: int, data: Dict) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/reject", json=data)

@handle_api_error
def send_invoice(invoice_id: int) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/send")

@handle_api_error
def send_invoice_to_circulation(invoice_id: int) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/sendToCirculation")

@handle_api_error
def set_invoice_unfinished(invoice_id: int) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/unfinished")

@handle_api_error
def verify_invoice(invoice_id: int, data: CommentEvent) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/verify", json=data.dict())

@handle_api_error
def confirm_action(transaction_identifier: str) -> requests.Response:
    return make_request("PUT", f"{PROCOUNTOR_URL}/invoices/{transaction_identifier}/confirm")