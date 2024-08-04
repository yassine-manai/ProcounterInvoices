import requests
from functions.check_error import handle_api_error
from config.config import PROCOUNTOR_URL
from functions.request_api import make_request

@handle_api_error
def remove_payment_event(invoice_id: int, payment_event_id: int) -> requests.Response:
    return make_request("DELETE", f"{PROCOUNTOR_URL}/invoices/{invoice_id}/paymentevents/{payment_event_id}")