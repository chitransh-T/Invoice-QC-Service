from typing import Dict, List, Any, Optional
from datetime import datetime
from schemas import ValidationResult, ValidationError, ValidationReport

class InvoiceValidator:
    """Validates extracted invoice data against business rules."""
    
    def __init__(self, tolerance: float = 0.01):
        """
        Initialize validator.
        tolerance: acceptable difference for totals calculations (default 0.01 EUR)
        """
        self.tolerance = tolerance
    
    def validate(self, invoices: List[Dict[str, Any]]) -> ValidationReport:
        """Validate a list of invoices and return aggregated report."""
        results = []
        error_summary = {}
        
        for invoice in invoices:
            result = self.validate_invoice(invoice)
            results.append(result)
            
            # Aggregate errors
            for error in result.errors + result.warnings:
                key = f"{error.field}: {error.message}"
                error_summary[key] = error_summary.get(key, 0) + 1
        
        valid_count = sum(1 for r in results if r.is_valid)
        invalid_count = len(results) - valid_count
        
        return ValidationReport(
            total_invoices=len(invoices),
            valid_invoices=valid_count,
            invalid_invoices=invalid_count,
            error_summary=error_summary,
            detailed_results=results
        )
    
    def validate_invoice(self, invoice: Dict[str, Any]) -> ValidationResult:
        """Validate a single invoice."""
        errors = []
        warnings = []
        
        # Completeness rules
        if not invoice.get('invoice_number'):
            errors.append(ValidationError(
                field='invoice_number',
                message='Invoice number is missing',
                severity='error'
            ))
        
        if not invoice.get('invoice_date'):
            errors.append(ValidationError(
                field='invoice_date',
                message='Invoice date is missing',
                severity='error'
            ))
        
        if not invoice.get('seller_name'):
            errors.append(ValidationError(
                field='seller_name',
                message='Seller name is missing',
                severity='error'
            ))
        
        if not invoice.get('buyer_name'):
            errors.append(ValidationError(
                field='buyer_name',
                message='Buyer name is missing',
                severity='error'
            ))
        
        # Format validation rules
        if invoice.get('invoice_date'):
            try:
                inv_date = datetime.strptime(invoice['invoice_date'], '%Y-%m-%d')
                # Check if date is reasonable (not too old, not in future)
                today = datetime.now()
                if (today - inv_date).days > 365 * 10:
                    warnings.append(ValidationError(
                        field='invoice_date',
                        message=f'Invoice date is more than 10 years old: {invoice["invoice_date"]}',
                        severity='warning'
                    ))
                if inv_date > today:
                    errors.append(ValidationError(
                        field='invoice_date',
                        message=f'Invoice date is in the future: {invoice["invoice_date"]}',
                        severity='error'
                    ))
            except ValueError:
                errors.append(ValidationError(
                    field='invoice_date',
                    message=f'Invalid date format: {invoice["invoice_date"]}',
                    severity='error'
                ))
        
        if invoice.get('due_date') and invoice.get('invoice_date'):
            try:
                inv_date = datetime.strptime(invoice['invoice_date'], '%Y-%m-%d')
                due_date = datetime.strptime(invoice['due_date'], '%Y-%m-%d')
                if due_date < inv_date:
                    errors.append(ValidationError(
                        field='due_date',
                        message='Due date is before invoice date',
                        severity='error'
                    ))
            except ValueError:
                pass
        
        # Currency validation
        valid_currencies = ['EUR', 'USD', 'GBP', 'CHF', 'CNY', 'JPY', 'INR']
        if invoice.get('currency') and invoice['currency'] not in valid_currencies:
            warnings.append(ValidationError(
                field='currency',
                message=f'Unknown currency: {invoice["currency"]}',
                severity='warning'
            ))
        
        # Business rules
        if invoice.get('gross_total') is not None:
            if invoice['gross_total'] <= 0:
                errors.append(ValidationError(
                    field='gross_total',
                    message='Gross total must be greater than 0',
                    severity='error'
                ))
        
        # Total calculations validation
        net = invoice.get('net_total')
        tax = invoice.get('tax_amount')
        gross = invoice.get('gross_total')
        
        if net is not None and tax is not None and gross is not None:
            calculated_gross = net + tax
            if abs(calculated_gross - gross) > self.tolerance:
                errors.append(ValidationError(
                    field='gross_total',
                    message=f'Totals mismatch: net ({net}) + tax ({tax}) = {calculated_gross}, but gross is {gross}',
                    severity='error'
                ))
        
        # Line items validation
        if invoice.get('line_items'):
            line_items_total = sum(item.get('line_total', 0) for item in invoice['line_items'])
            if net is not None and line_items_total > 0:
                if abs(line_items_total - net) > self.tolerance:
                    warnings.append(ValidationError(
                        field='line_items',
                        message=f'Line items total ({line_items_total}) does not match net total ({net})',
                        severity='warning'
                    ))
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            invoice_number=invoice.get('invoice_number', 'UNKNOWN'),
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
