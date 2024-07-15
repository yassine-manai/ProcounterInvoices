from enum import Enum

class Status(Enum):
    EMPTY = "EMPTY"
    UNFINISHED = "UNFINISHED"
    NOT_SENT = "NOT_SENT"
    SENT = "SENT"
    RECEIVED = "RECEIVED"
    PAID = "PAID"
    PAYMENT_DENIED = "PAYMENT_DENIED"
    VERIFIED = "VERIFIED"
    APPROVED = "APPROVED"
    INVALIDATED = "INVALIDATED"
    PAYMENT_QUEUED = "PAYMENT_QUEUED"
    PARTLY_PAID = "PARTLY_PAID"
    PAYMENT_SENT_TO_BANK = "PAYMENT_SENT_TO_BANK"
    MARKED_PAID = "MARKED_PAID"
    STARTED = "STARTED"
    INVOICED = "INVOICED"
    OVERRIDDEN = "OVERRIDDEN"
    DELETED = "DELETED"
    UNSAVED = "UNSAVED"
    PAYMENT_TRANSACTION_REMOVED = "PAYMENT_TRANSACTION_REMOVED"
