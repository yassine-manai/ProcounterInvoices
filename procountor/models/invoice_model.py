import datetime as dt
from typing import List, Optional
from pydantic import BaseModel, Field
from procountor.enum.country_Enum import Country
from procountor.enum.currency_Enum import CurrencyCode
from procountor.enum.payment_Enum import PaymentMeth, PaymentMethType
from procountor.enum.short_Enum import DeliveryMethod, DocumentInvoiceType, InvoiceSendingMethod, Language, PaymentType, ReferenceType, cashDiscountsType
from procountor.enum.status_Enum import Status
from procountor.enum.unitProduct_Enum import UnitProduct


class InvoiceCounterpartyAddress(BaseModel):
    name: str = Field(default="Sample Name", max_length=80, min_length=0)
    specifier: Optional[str] = Field(default="Sample Specifier", max_length=80, min_length=0)
    street: Optional[str] = Field(default="Sample Street", max_length=80, min_length=0)
    zip: Optional[str] = Field(default="12345", max_length=20, min_length=0)
    city: Optional[str] = Field(default="Sample City", max_length=40, min_length=0)
    country: Optional[Country] = Field(default=Country.SWEDEN, example="SWEDEN")
    subdivision: Optional[str] = Field(default="Sample Subdivision", max_length=35)
    
class BankAccount(BaseModel):
    accountNumber: Optional[str] = "123456789"
    bic: Optional[str] = "SAMPLEBIC"    
    
    
class EInvoiceAddress(BaseModel):
    operator: Optional[str] = "Sample Operator"
    address: Optional[str] = "Sample Address"
    ediId: Optional[str] = "SAMPLEEDI"

class CounterParty(BaseModel):
    contactPersonName: Optional[str] = "Yassine"
    identifier: Optional[str] = "1460"
    taxCode: Optional[str] = "123456"
    customerNumber: Optional[str] = "0147"
    email: Optional[str] = "yassinemanai955@gmail.com"
    counterPartyAdress: InvoiceCounterpartyAddress = InvoiceCounterpartyAddress()
    bankAccount: Optional[BankAccount] = BankAccount()


class InvoiceBillingAddress(BaseModel):
    name: str = Field(default="Sample Billing Name", max_length=80, min_length=0)
    specifier: Optional[str] = Field(default="Sample Specifier", max_length=80, min_length=0)
    street: Optional[str] = Field(default="Sample Billing Street", max_length=80, min_length=0)
    zip: Optional[str] = Field(default="54321", max_length=20, min_length=0)
    city: Optional[str] = Field(default="Sample Billing City", max_length=40, min_length=0)
    country: Country = Field(default=Country.SWEDEN, example="SWEDEN")
    subdivision: Optional[str] = Field(default="Sample Billing Subdivision", max_length=35)

class InvoiceDeliveryAddress(BaseModel):
    name: str = Field(default="Sample Delivery Name", max_length=80, min_length=0)
    specifier: Optional[str] = Field(default="Sample Specifier", max_length=80, min_length=0)
    street: Optional[str] = Field(default="Sample Delivery Street", max_length=80, min_length=0)
    zip: Optional[str] = Field(default="98765", max_length=20, min_length=0)
    city: Optional[str] = Field(default="Sample Delivery City", max_length=40, min_length=0)
    country: Country = Field(default=Country.SWEDEN, example="SWEDEN")
    subdivision: Optional[str] = Field(default="Sample Delivery Subdivision", max_length=35)

class BankAccountPaymentInfo(BaseModel):
    bankAccount: Optional[BankAccount] = BankAccount()

class CashDiscountOption(BaseModel):
    description: str = "Sample Discount Description"
    numberOfDays: int = 10
    discountPercentage: float = 5.0

class CashDiscount(BaseModel):
    optionList: Optional[List[CashDiscountOption]] = [CashDiscountOption()]
    cashDiscountsTermType: cashDiscountsType = cashDiscountsType.FROM_INV_DATE

class PaymentInfo(BaseModel):
    paymentMethod: PaymentMeth = PaymentMeth.BANK_TRANSFER
    currency: CurrencyCode = Field(default="EUR", example="EUR")
    bankAccount: Optional[BankAccountPaymentInfo] = BankAccountPaymentInfo()
    dueDate: str = Field(default="2024-08-01", description="Payment due date.")
    currencyRate: float = 1.0
    paymentTermPercentage: Optional[float] = 10.0
    cashDiscount: Optional[CashDiscount] = CashDiscount()
    bankReferenceCode: Optional[str] = "123456"
    bankReferenceCodeType: PaymentType = PaymentType.RF

class TravelInformationItem(BaseModel):
    departure: Optional[str] = "Sample Departure"
    arrival: Optional[str] = "Sample Arrival"
    places: Optional[str] = "Sample Places"
    purpose: Optional[str] = "Sample Purpose"

class InvoiceCheckerInformation(BaseModel):
    userId: int = 1
    eventPerformed: Optional[str] = "Sample Event"

class InvoiceApprovalInformation(BaseModel):
    acceptors: Optional[List[InvoiceCheckerInformation]] = [InvoiceCheckerInformation()]
    verifiers: Optional[List[InvoiceCheckerInformation]] = [InvoiceCheckerInformation()]

class Attachment(BaseModel):
    id: int = 1
    name: str = "Sample Attachment"
    referenceType: ReferenceType = ReferenceType.ENVIRONMENT
    referenceId: int = 123
    mimeType: Optional[str] = "application/pdf"
    sendWithInvoice: bool = True
    attachmentInvoice: str = "Sample Attachment Invoice"
    	
class ExtraInfo(BaseModel):
    accountingByRow: bool = True
    unitPricesIncludeVat: bool = False

class DelevryTermsInfo(BaseModel):
    name: Optional[str] = "Sample Delivery Terms Name"
    municipality: Optional[str] = "Sample Municipality"
    
class InvoiceOperatorInfo(BaseModel):
    operator: str = "Sample Operator"
    receivingAddress: str = "Sample Receiving Address"
    
class InvoiceRow(BaseModel):
    id: Optional[int] = 1
    productId: Optional[int] = 101
    product: str = "Sample Product"
    productCode: Optional[str] = "PROD123"
    quantity: float = 1.0
    unit: UnitProduct = UnitProduct.BAG
    unitPrice: float = 100.0
    discountPercent: Optional[float] = 10.0
    vatPercent: float = 20.0
    vatStatus: Optional[int] = 1
    comment: Optional[str] = "Sample Comment"
    startDate: Optional[str] = "2024-07-01"
    endDate: Optional[str] = "2024-07-31"
    headerText: Optional[str] = "Sample Header Text"
    explanationText: Optional[str] = "Sample Explanation Text"

class Invoice(BaseModel):
    partnerId: Optional[int] = 123
    type: DocumentInvoiceType = DocumentInvoiceType.BILL_OF_CHARGES
    status: Status = Status.UNFINISHED
    date: str = "2024-07-01"
    paymentDate: Optional[str] = "2024-07-02"
    counterParty: Optional[CounterParty] = CounterParty()
    billingAddress: Optional[InvoiceBillingAddress] = InvoiceBillingAddress()
    deliveryAddress: Optional[InvoiceDeliveryAddress] = InvoiceDeliveryAddress()
    paymentInfo: PaymentInfo = PaymentInfo()
    deliveryTermsInfo: DelevryTermsInfo = DelevryTermsInfo()
    extraInfo: ExtraInfo = ExtraInfo()
    discountPercent: float = 5.0
    orderReference: Optional[str] = "ORD123"
    invoiceRows: List[InvoiceRow] = [InvoiceRow()]
    invoiceNumber: Optional[int] = 456
    vatStatus: Optional[int] = 2
    originalInvoiceNumber: Optional[str] = "INV123"
    deliveryStartDate: Optional[str] = "2024-07-01"
    deliveryEndDate: Optional[str] = "2024-07-31"
    deliveryMethod: DeliveryMethod = DeliveryMethod.BUS
    deliveryInstructions: Optional[str] = "Sample Delivery Instructions"
    invoiceChannel: InvoiceSendingMethod = InvoiceSendingMethod.EMAIL
    invoiceOperatorInfo: Optional[InvoiceOperatorInfo] = InvoiceOperatorInfo()
    penaltyPercent: Optional[float] = 1.5
    language: Optional[Language] = Language.ENGLISH
    invoiceTemplateId: Optional[int] = 789
    additionalInformation: Optional[str] = "Sample Additional Information"
    vatCountry: Optional[str] = "SWEDEN"
    ledgerReceiptId: Optional[int] = 1234
    notes: Optional[str] = "Sample Notes"
    factoringContractId: Optional[int] = 5678
    factoringText: Optional[str] = "Sample Factoring Text"
    sum: Optional[float] = 1000.0
    travelInformationItems: Optional[List[TravelInformationItem]] = [TravelInformationItem()]
    invoiceApprovalInformation: Optional[InvoiceApprovalInformation] = InvoiceApprovalInformation()
    attachments: Optional[List[Attachment]] = [Attachment()]
    orderNumber: Optional[str] = "ORD123"
    agreementNumber: Optional[str] = "AGR123"
    accountingCode: Optional[str] = "ACC123"
    deliverySite: Optional[str] = "Sample Delivery Site"
    tenderReference: Optional[str] = "TEND123"
    version: Optional[str] = "1.0"
    isOffer: Optional[bool] = False





class CommentDTO(BaseModel):
    id: Optional[int] = 1
    author: Optional[str] = "Sample Author"
    dateTime: Optional[dt.datetime] = dt.datetime.now()
    comment: str = "Sample Comment"
    
class MarkInvoiceAsPaid(BaseModel):
    paymentDate: str = Field(default="2024-07-01", description="Payment date. Cannot be in closed financial period")
    amount: float = Field(default=100.0, description="Amount in the given currency")
    currency: CurrencyCode = Field(default="EUR", description="Currency in ISO 4217 format. It should always be the same as in the invoice")
    description: Optional[str] = Field(default="Sample Payment Description", max_length=140, description="Payment description. Used only in sales invoices.")
    paymentMethodType: Optional[PaymentMethType] = Field(default=PaymentMethType.CASH, description="Payment method type. Used only in sales invoices.")
    
    
class CommentEvent(BaseModel):
    comment: Optional[str] = Field(default="Sample Comment for Event", max_length=100, description="Comment for verification or approval event.")

class ResultsInvoice(BaseModel):
    id: int = 1
    partnerId: int = 123
    typeInvoice: DocumentInvoiceType = DocumentInvoiceType.SALES_INVOICE
    status: Status = Status.STARTED
    invoiceNumber: int = 456 
    originalInvoiceNumber: str = "INV123"
    invoiceChannel: InvoiceSendingMethod = InvoiceSendingMethod.EMAIL
    date: str = "2024-07-01"
    dueDate: str = "2024-08-01"
    created: str = dt.datetime.now().isoformat()
    version: str = dt.datetime.now().isoformat()

class MetaInvoice(BaseModel):
    pageNumber: int = 1
    pageSize: int = 10
    resultCount: int = 1
    totalCount: int = 100
     
class InvoiceSearchResult(BaseModel):
    results: ResultsInvoice = ResultsInvoice()
    meta: MetaInvoice = MetaInvoice()
