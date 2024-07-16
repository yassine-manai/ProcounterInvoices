import datetime as dt
from typing import List, Optional
from pydantic import BaseModel, Field
from procountor.enum.country_Enum import Country
from procountor.enum.currency_Enum import CurrencyCode
from procountor.enum.payment_Enum import PaymentMeth, PaymentMethType
from procountor.enum.short_Enum import DeliveryMethod, DocumentInvoiceType, InvoiceSendingMethod, Language, PaymentType, ReferenceType, cashDiscountsType
from procountor.enum.status_Enum import Status
from procountor.enum.unitProduct_Enum import UnitProduct


class CounterParty(BaseModel):
    description: Optional[str]
    contactPersonName: Optional[str]
    identifier: Optional[str]
    taxCode: Optional[str]
    customerNumber: Optional[str]
    email: Optional[str]

class InvoiceCounterpartyAddress(BaseModel):
    name: str = Field(max_length=80, min_length=0)
    specifier: Optional[str] = Field(max_length=80, min_length=0)
    street: Optional[str] = Field(max_length=80, min_length=0)
    zip: Optional[str] = Field(max_length=20, min_length=0)
    city: Optional[str] = Field(max_length=40, min_length=0)
    country: Optional[str] = Field(example="SWEDEN")
    subdivision: Optional[str] = Field(max_length=35)

class BankAccount(BaseModel):
    accountNumber: Optional[str]
    bic: Optional[str]

class EInvoiceAddress(BaseModel):
    operator: Optional[str]
    address: Optional[str]
    ediId: Optional[str]

class InvoiceBillingAddress(BaseModel):
    name: str = Field(max_length=80, min_length=0)
    specifier: Optional[str] = Field(max_length=80, min_length=0)
    street: Optional[str] = Field(max_length=80, min_length=0)
    zip: Optional[str] = Field(max_length=20, min_length=0)
    city: Optional[str] = Field(max_length=40, min_length=0)
    country: Country[str] = Field(example="SWEDEN")
    subdivision: Optional[str] = Field(max_length=35)

class InvoiceDeliveryAddress(BaseModel):
    name: str = Field(max_length=80, min_length=0)
    specifier: Optional[str] = Field(max_length=80, min_length=0)
    street: Optional[str] = Field(max_length=80, min_length=0)
    zip: Optional[str] = Field(max_length=20, min_length=0)
    city: Optional[str] = Field(max_length=40, min_length=0)
    country: Country[str] = Field(example="SWEDEN")
    subdivision: Optional[str] = Field(max_length=35)

class BankAccountPaymentInfo(BaseModel):
    bankAccount: Optional[BankAccount]

class CashDiscountOption(BaseModel):
    description: str
    numberOfDays: int
    discountPercentage: float

class CashDiscount(BaseModel):
    optionList: Optional[List[CashDiscountOption]]
    cashDiscountsTermType: cashDiscountsType

class PaymentInfo(BaseModel):
    paymentMethod: PaymentMeth
    currency: CurrencyCode = Field(example="EUR")
    bankAccount: Optional[BankAccountPaymentInfo]
    dueDate: str = Field(description="Payment due date.")
    currencyRate: float
    paymentTermPercentage: Optional[float]
    cashDiscount: Optional[CashDiscount]
    bankReferenceCode: Optional[str]
    bankReferenceCodeType: PaymentType
    clearingCode: Optional[str]

class TravelInformationItem(BaseModel):
    departure: Optional[str]
    arrival: Optional[str]
    places: Optional[str]
    purpose: Optional[str]

class InvoiceCheckerInformation(BaseModel):
    userId: int
    eventPerformed: Optional[str]

class InvoiceApprovalInformation(BaseModel):
    acceptors: Optional[List[InvoiceCheckerInformation]]
    verifiers: Optional[List[InvoiceCheckerInformation]]

class Attachment(BaseModel):
    id: int
    name: str
    referenceType: ReferenceType
    referenceId: int
    mimeType: Optional[str]
    sendWithInvoice: bool
    attachmentInvoice: str
    	
class ExtraInfo(BaseModel):
    accountingByRow: bool
    unitPricesIncludeVat: bool

class DelevryTermsInfo(BaseModel):
    name: Optional[str]
    municipality: Optional[str]
    
class InvoiceOperatorInfo(BaseModel):
    operator: str
    receivingAddress: str
    
class InvoiceRow(BaseModel):
    id: Optional[int]
    productId: Optional[int]
    product: str
    productCode: Optional[str]
    quantity: float
    unit: UnitProduct
    unitPrice: float
    discountPercent: Optional[float]
    vatPercent: float
    vatStatus: Optional[int]
    comment: Optional[str]
    startDate: Optional[str]
    endDate: Optional[str]
    headerText: Optional[str]
    explanationText: Optional[str]

class Invoice(BaseModel):
    id: Optional[int]
    partnerId: Optional[int]
    invoiceType: DocumentInvoiceType
    status: Status
    date: str = Field(description="Invoice date.")
    paymentDate: Optional[str]
    counterParty: Optional[CounterParty]
    counterPartyAddress: Optional[InvoiceCounterpartyAddress]
    billingAddress: Optional[InvoiceBillingAddress]
    deliveryAddress: Optional[InvoiceDeliveryAddress]
    paymentInfo: PaymentInfo
    deliveryTermsInfo: DelevryTermsInfo
    extraInfo: ExtraInfo
    discountPercent: float
    orderReference: Optional[str]
    invoiceRows: List[InvoiceRow]
    invoiceNumber: Optional[int]
    vatStatus: Optional[int]
    originalInvoiceNumber: Optional[str]
    deliveryStartDate: Optional[str]
    deliveryEndDate: Optional[str]
    deliveryMethod: DeliveryMethod
    deliveryInstructions: Optional[str]
    invoiceChannel: str
    invoiceOperatorInfo: Optional[InvoiceOperatorInfo]
    penaltyPercent: Optional[float]
    language: Optional[Language]
    invoiceTemplateId: Optional[int]
    additionalInformation: Optional[str]
    vatCountry: Optional[str]
    ledgerReceiptId: Optional[int]
    notes: Optional[str]
    factoringContractId: Optional[int]
    factoringText: Optional[str]
    sumData: Optional[float]
    travelInformationItems: Optional[List[TravelInformationItem]]
    invoiceApprovalInformation: Optional[InvoiceApprovalInformation]
    attachments: Optional[List[Attachment]]
    orderNumber: Optional[str]
    agreementNumber: Optional[str]
    accountingCode: Optional[str]
    deliverySite: Optional[str]
    tenderReference: Optional[str]
    version: Optional[str]
    isOffer: Optional[bool]
    
    
class CommentDTO(BaseModel):
    id: Optional[int]
    author: Optional[str]
    dateTime: Optional[dt.datetime]
    comment: str
    
class MarkInvoiceAsPaid(BaseModel):
    paymentDate: str = Field(..., description="Payment date. Cannot be in closed financial period")
    amount: float = Field(..., description="Amount in the given currency")
    currency: CurrencyCode = Field(..., description="Currency in ISO 4217 format. It should always be the same as in the invoice")
    description: Optional[str] = Field(None, max_length=140, description="Payment description. Used only in sales invoices.")
    paymentMethodType: Optional[PaymentMethType] = Field(None, description="Payment method type. Used only in sales invoices.")
    
    
class CommentEvent(BaseModel):
    comment: Optional[str] = Field(None, max_length=100, description="Comment for verification or approval event.")


class resultsInvoice(BaseModel):
    id : int
    partnerId: int
    typeInvoice: DocumentInvoiceType
    status: Status
    invoiceNumber: int 
    originalInvoiceNumber: str
    invoiceChannel: InvoiceSendingMethod
    date: str[dt.date]
    dueDate: str[dt.date]
    created:str[dt.datetime]
    version: str[dt.datetime]
    

class metaInvoice(BaseModel):
    pageNumber: int
    pageSize: int
    resultCount: int
    totalCount: int
     
class invoiceSearchResult(BaseModel):
    results: resultsInvoice
    meta: metaInvoice
    

