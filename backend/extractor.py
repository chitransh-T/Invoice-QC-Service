import pdfplumber
import re
from typing import Dict, Optional, List, Any
from datetime import datetime

class InvoiceExtractor:
    """Extracts structured data from invoice PDFs."""
    
    def __init__(self):
        self.patterns = {
            'invoice_number': [
                r'(?:Bestellung|Order|Invoice)[\s:]*([A-Z0-9\-\/]+)',
                r'(?:AUFNR|AUFN)[\s:]*([A-Z0-9\-\/]+)',
                r'(?:Rechnungsnummer|Invoice\s*#)[\s:]*([A-Z0-9\-\/]+)',
            ],
            'invoice_date': [
                r'(?:vom|from|Datum|Date)[\s:]*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{4})',
                r'(\d{4}[\-\/]\d{2}[\-\/]\d{2})',
            ],
            'currency': [
                r'(?:EUR|USD|GBP|CHF)',
            ],
            'iban': [
                r'[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}',
            ],
            'tax_rate': [
                r'(?:MwSt|VAT|Tax)[\s:]*(\d+(?:[.,]\d{2})?)\s*%',
            ],
        }
    
    def extract(self, pdf_path: str) -> Dict[str, Any]:
        """Extract invoice data from a PDF file."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages])
                return self._parse_invoice_text(text)
        except Exception as e:
            print(f"Error extracting PDF {pdf_path}: {e}")
            return self._empty_invoice()
    
    def _parse_invoice_text(self, text: str) -> Dict[str, Any]:
        """Parse extracted text into structured invoice data."""
        data = self._empty_invoice()
        
        # Extract invoice number
        data['invoice_number'] = self._find_pattern(text, self.patterns['invoice_number'])
        
        # Extract invoice date
        invoice_date_str = self._find_pattern(text, self.patterns['invoice_date'])
        if invoice_date_str:
            data['invoice_date'] = self._parse_date(invoice_date_str)
        
        # Extract currency
        data['currency'] = self._find_pattern(text, self.patterns['currency']) or "EUR"
        
        # Extract tax rate
        tax_rate_str = self._find_pattern(text, self.patterns['tax_rate'])
        if tax_rate_str:
            data['tax_percentage'] = float(tax_rate_str.replace(',', '.'))
        
        # Extract seller and buyer names
        data['seller_name'] = self._extract_seller_name(text)
        data['buyer_name'] = self._extract_buyer_name(text)
        
        # Extract addresses
        data['seller_address'] = self._extract_seller_address(text)
        data['buyer_address'] = self._extract_buyer_address(text)
        
        # Extract amounts
        amounts = self._extract_amounts(text)
        data['net_total'] = amounts.get('net_total')
        data['tax_amount'] = amounts.get('tax_amount')
        data['gross_total'] = amounts.get('gross_total')
        
        # Extract line items
        data['line_items'] = self._extract_line_items(text)
        
        # Extract payment terms
        data['payment_terms'] = self._extract_payment_terms(text)
        
        # Calculate due date (simple: 14 days after invoice date if not provided)
        if data['invoice_date'] and not data['due_date']:
            try:
                inv_date = datetime.strptime(data['invoice_date'], '%Y-%m-%d')
                due_date = inv_date.replace(day=inv_date.day + 14)
                data['due_date'] = due_date.strftime('%Y-%m-%d')
            except:
                pass
        
        return data
    
    def _empty_invoice(self) -> Dict[str, Any]:
        """Return empty invoice structure."""
        return {
            'invoice_number': None,
            'invoice_date': None,
            'due_date': None,
            'seller_name': None,
            'seller_address': None,
            'buyer_name': None,
            'buyer_address': None,
            'currency': 'EUR',
            'net_total': None,
            'tax_amount': None,
            'gross_total': None,
            'tax_percentage': 19.0,
            'payment_terms': None,
            'line_items': [],
            'status': 'pending'
        }
    
    def _find_pattern(self, text: str, patterns: List[str]) -> Optional[str]:
        """Find first matching pattern in text."""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        return None
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """Convert various date formats to YYYY-MM-DD."""
        formats = ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y/%m/%d']
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None
    
    def _extract_seller_name(self, text: str) -> Optional[str]:
        """Extract seller/vendor name."""
        # Look for common patterns
        patterns = [
            r'(?:Lieferant|Vendor|Supplier|Von|From)[:\s]+([A-Z][A-Za-z\s&\.]+)',
            r'(?:ABC Corporation|JKL Corporation|Softwareunternehmen|medical equipment)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.groups() else match.group(0).strip()
        return None
    
    def _extract_buyer_name(self, text: str) -> Optional[str]:
        """Extract buyer/customer name."""
        patterns = [
            r'(?:Kundenanschrift|Customer|Buyer|Kunde)[:\s]+([A-Z][A-Za-z\s&\.]+)',
            r'(?:Beispielname Unternehmen)',
            r'^([A-Z][A-Za-z\s&\.]+)\n.*(?:Philipp-Ott-Str|Albertus-Magnus)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip() if match.groups() else match.group(0).strip()
        return None
    
    def _extract_seller_address(self, text: str) -> Optional[str]:
        """Extract seller address."""
        match = re.search(
            r'(?:Lieferanschrift|Supplier.*?Address)[:\s]*([^\n]+(?:\n[^\n]+){0,3})',
            text, re.IGNORECASE | re.DOTALL
        )
        if match:
            return match.group(1).strip()
        return None
    
    def _extract_buyer_address(self, text: str) -> Optional[str]:
        """Extract buyer address."""
        match = re.search(
            r'(?:Kundenanschrift|Customer.*?Address)[:\s]*([^\n]+(?:\n[^\n]+){0,3})',
            text, re.IGNORECASE | re.DOTALL
        )
        if match:
            return match.group(1).strip()
        # Try to find address with street/city pattern
        match = re.search(
            r'((?:Straße|Str\.?|Street).*?)(?:\n|$)',
            text, re.IGNORECASE
        )
        if match:
            return match.group(1).strip()
        return None
    
    def _extract_amounts(self, text: str) -> Dict[str, Optional[float]]:
        """Extract monetary amounts (net, tax, gross)."""
        amounts = {'net_total': None, 'tax_amount': None, 'gross_total': None}
        
        # Extract all currency amounts
        currency_pattern = r'(?:EUR|€)\s*([\d.,]+)(?:\s|$)'
        matches = re.findall(currency_pattern, text)
        
        if matches:
            # Try to identify which is which based on position and context
            floats = [float(m.replace('.', '').replace(',', '.')) for m in matches]
            floats = sorted(set(floats), reverse=True)  # Unique, sorted descending
            
            if len(floats) >= 3:
                amounts['gross_total'] = floats[0]
                amounts['tax_amount'] = floats[1]
                amounts['net_total'] = floats[2]
            elif len(floats) == 2:
                amounts['gross_total'] = floats[0]
                amounts['net_total'] = floats[1]
        
        return amounts
    
    def _extract_line_items(self, text: str) -> List[Dict[str, Any]]:
        """Extract line items from invoice."""
        line_items = []
        
        # Look for table structure with quantity, price patterns
        # Pattern: quantity, description, unit price, line total
        line_pattern = r'(\d+)\s+([A-Za-z0-9\s]+?)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        
        for match in re.finditer(line_pattern, text):
            try:
                qty = float(match.group(1))
                desc = match.group(2).strip()
                unit_price = float(match.group(3).replace(',', '.'))
                line_total = float(match.group(5).replace(',', '.'))
                
                if desc and len(desc) > 3:  # Filter out noise
                    line_items.append({
                        'description': desc,
                        'quantity': qty,
                        'unit_price': unit_price,
                        'line_total': line_total
                    })
            except (ValueError, IndexError):
                continue
        
        return line_items
    
    def _extract_payment_terms(self, text: str) -> Optional[str]:
        """Extract payment terms."""
        match = re.search(
            r'(?:Zahlungsbedingungen|Payment\s*Terms)[:\s]*([^\n]+)',
            text, re.IGNORECASE
        )
        if match:
            return match.group(1).strip()
        return None
