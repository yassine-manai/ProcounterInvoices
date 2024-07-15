# Invoices Endpoints
import requests
from typing import Any, Dict, List, Union
from config.config import PROCOUNTOR_URL


def get_invoices(params: Dict[str, Any] = None) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices"
    response = requests.get(url, params=params)
    return response

def create_invoice(data: Dict[str, Any]) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices"
    response = requests.post(url, json=data)
    return response

def get_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}"
    response = requests.get(url)
    return response

def update_invoice(invoice_id: str, data: Dict[str, Any]) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}"
    response = requests.put(url, json=data)
    return response

def approve_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/approve"
    response = requests.put(url)
    return response

def get_invoice_comments(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments"
    response = requests.get(url)
    return response

def add_invoice_comment(invoice_id: str, data: Dict[str, Any]) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments"
    response = requests.post(url, json=data)
    return response

def get_taggable_users(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/comments/taggableusers"
    response = requests.get(url)
    return response

def get_invoice_image(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/image"
    response = requests.get(url)
    return response

def invalidate_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/invalidate"
    response = requests.put(url)
    return response

def update_invoice_notes(invoice_id: str, data: Dict[str, Any]) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/notes"
    response = requests.put(url, json=data)
    return response

def get_payment_events(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents"
    response = requests.get(url)
    return response

def get_payment_event(invoice_id: str, payment_event_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/{payment_event_id}"
    response = requests.get(url)
    return response

def remove_payment_event(invoice_id: str, payment_event_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/{payment_event_id}"
    response = requests.delete(url)
    return response

def mark_invoice_paid(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/markpaid"
    response = requests.put(url)
    return response

def reject_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/reject"
    response = requests.put(url)
    return response

def send_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/send"
    response = requests.put(url)
    return response

def send_invoice_to_circulation(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/sendToCirculation"
    response = requests.put(url)
    return response

def get_invoice_transactions(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/transactions"
    response = requests.get(url)
    return response

def set_invoice_unfinished(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/unfinished"
    response = requests.put(url)
    return response

def verify_invoice(invoice_id: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{invoice_id}/verify"
    response = requests.put(url)
    return response

def confirm_action(transaction_identifier: str) -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/{transaction_identifier}/confirm"
    response = requests.put(url)
    return response

def get_personal_approvals() -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/personalapprovals"
    response = requests.get(url)
    return response

def get_personal_verifications() -> requests.Response:
    url = f"{PROCOUNTOR_URL}/invoices/personalverifications"
    response = requests.get(url)
    return response
