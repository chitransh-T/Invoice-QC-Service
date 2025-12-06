from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class LineItem(BaseModel):
    """Schema for a line item in an invoice."""
    description: str
    quantity: float
    unit_price: float
    line_total: float

class InvoiceData(BaseModel):
    """Schema for extracted invoice data."""
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    seller_name: Optional[str] = None
    seller_address: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_address: Optional[str] = None
    currency: Optional[str] = "EUR"
    net_total: Optional[float] = None
    tax_amount: Optional[float] = None
    gross_total: Optional[float] = None
    tax_percentage: Optional[float] = 19.0
    payment_terms: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    status: str = "pending"

class ValidationError(BaseModel):
    """Schema for validation errors."""
    field: str
    message: str
    severity: str = "error"  # error or warning

class ValidationResult(BaseModel):
    """Schema for validation results per invoice."""
    invoice_number: Optional[str]
    is_valid: bool
    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

class ValidationReport(BaseModel):
    """Schema for aggregated validation report."""
    total_invoices: int
    valid_invoices: int
    invalid_invoices: int
    error_summary: dict = {}
    detailed_results: List[ValidationResult] = []
