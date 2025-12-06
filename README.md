# Invoice QC Service - Proof of Concept

A complete B2B invoice extraction and quality control system with FastAPI backend and React frontend.

## 📋 Overview

This PoC demonstrates:
- **PDF Extraction**: Intelligent extraction of structured invoice data from German B2B invoices
- **Validation Engine**: Comprehensive business rule validation (completeness, format, calculations)
- **CLI Tool**: Command-line interface for batch processing
- **REST API**: FastAPI backend with CORS support
- **React UI**: Modern, responsive web interface for invoice analysis

## ✅ Completed Components

- ✓ Backend: FastAPI with PDF extraction & validation
- ✓ Frontend: React with Tailwind CSS
- ✓ CLI: Multi-command tool (extract, validate, full-run)
- ✓ API: RESTful endpoints for analysis
- ✓ UI: Real-time invoice processing with results display

## 📊 Schema & Validation Design

### Extracted Fields

**Invoice-level fields:**
- `invoice_number`: Unique invoice identifier (e.g., AUFNR34343)
- `invoice_date`: Invoice issuance date (YYYY-MM-DD)
- `due_date`: Payment due date (calculated from invoice date if not found)
- `seller_name`: Vendor/supplier name
- `seller_address`: Vendor address
- `buyer_name`: Customer/buyer name
- `buyer_address`: Customer address
- `currency`: Transaction currency (EUR, USD, etc.)
- `net_total`: Amount before tax
- `tax_amount`: Tax/VAT amount
- `gross_total`: Total amount including tax
- `tax_percentage`: Tax rate (default 19% for German invoices)
- `payment_terms`: Payment conditions
- `status`: Invoice processing status

**Line items:**
- `description`: Product/service description
- `quantity`: Item quantity
- `unit_price`: Price per unit
- `line_total`: Total for line item

### Validation Rules

**Completeness Rules** (must have):
- Invoice number must not be empty
- Invoice date must be present and valid
- Seller name must not be empty
- Buyer name must not be empty

**Format Rules:**
- Invoice date must be in valid date format (multiple formats supported)
- Currency must be in known set (EUR, USD, GBP, CHF, CNY, JPY, INR)
- Due date must be on or after invoice date
- Invoice date should not be more than 10 years old

**Business Rules:**
- Gross total must be > 0
- `gross_total` must approximately equal `net_total + tax_amount` (tolerance: ±0.01)
- Line items total should match net total
- Tax amount should match net total × tax percentage

**Anomaly Rules:**
- Flag invoices with dates in the future
- Flag unknown currencies
- Flag mismatched totals

## 🏗️ Architecture

\`\`\`
PDF → Extraction (pdfplumber + regex) → JSON
                                          ↓
                                    Validation Engine
                                          ↓
                                    Quality Report
                                    
Components:
- extractor.py:  Regex-based field extraction from text
- validator.py:  Business rule validation engine
- schemas.py:    Pydantic models for type safety
- main.py:       FastAPI REST API server
- cli.py:        CLI tool for batch processing
- React UI:      Upload, visualize, and validate invoices
\`\`\`

### Extraction Pipeline
1. PDF → Raw text (pdfplumber)
2. Pattern matching for each field group (dates, amounts, names)
3. Text heuristics for buyer/seller identification
4. Amount parsing with multiple format support
5. Structured JSON output

### Validation Pipeline
1. Per-invoice rule checking
2. Error/warning categorization
3. Aggregated summary generation
4. Detailed per-field error messages

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)

### Backend Setup

\`\`\`bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run FastAPI server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

The API will be available at `http://localhost:8000`

### Frontend Setup

\`\`\`bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
\`\`\`

The UI will open at `http://localhost:5173`

## 💻 Usage

### REST API

**Health Check:**
\`\`\`bash
curl http://localhost:8000/health
\`\`\`

**Analyze Single Invoice (with file upload):**
\`\`\`bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@sample_invoice.pdf"
\`\`\`

**Validate JSON Invoices:**
\`\`\`bash
curl -X POST http://localhost:8000/api/validate-json \
  -H "Content-Type: application/json" \
  -d '[{"invoice_number":"INV-001",...}]'
\`\`\`

**Extract & Validate Multiple PDFs:**
\`\`\`bash
curl -X POST http://localhost:8000/api/extract-and-validate \
  -F "files=@invoice1.pdf" \
  -F "files=@invoice2.pdf"
\`\`\`

### CLI Tool

**Extract PDFs only:**
\`\`\`bash
python -m backend.cli extract --pdf-dir ./pdfs --output invoices.json
\`\`\`

**Validate extracted data:**
\`\`\`bash
python -m backend.cli validate-cmd --input invoices.json --report report.json
\`\`\`

**Full extraction + validation pipeline:**
\`\`\`bash
python -m backend.cli full-run --pdf-dir ./pdfs --report report.json
\`\`\`

### Web UI

1. Open http://localhost:5173
2. Click "Choose PDF" to upload an invoice
3. View validation results and extracted data
4. Switch between "Validation Results" and "Extracted Data" tabs

## 🔗 Integration Notes

### Embedding in Larger Systems

**API Integration:**
\`\`\`javascript
// Call from any service
fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  body: formData  // Contains PDF file
})
.then(res => res.json())
.then(data => {
  console.log('Extracted:', data.extracted);
  console.log('Validation:', data.validation);
})
\`\`\`

**Batch Processing Pipeline:**
\`\`\`python
from backend.extractor import InvoiceExtractor
from backend.validator import InvoiceValidator

extractor = InvoiceExtractor()
validator = InvoiceValidator()

# Process batch
for pdf_path in pdf_files:
    data = extractor.extract(pdf_path)
    result = validator.validate_invoice(data)
    if result.is_valid:
        # Continue to billing/accounting system
\`\`\`

**Queue Integration (Celery/RQ):**
\`\`\`python
# Could be called from message queue
@task
def process_invoice(pdf_url):
    pdf_path = download_pdf(pdf_url)
    data = extractor.extract(pdf_path)
    result = validator.validate(data)
    return result.dict()
\`\`\`

**Containerization:**
\`\`\`dockerfile
FROM python:3.11
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

## ⚠️ Assumptions & Limitations

### Simplifications (by design)
- **Regex-based extraction**: Works well for structured PDFs; complex/scanned documents need OCR
- **Limited line item support**: Extracts basic quantity/price; complex tables may be missed
- **German invoice focus**: Patterns optimized for German B2B invoices; adapt for other formats
- **Tax calculation**: Assumes single tax rate; complex multi-rate invoices not fully supported

### Known Edge Cases
- **Scanned/image PDFs**: Require OCR (consider pytesseract for production)
- **Handwritten fields**: Not supported
- **Multiple currencies**: Single currency per invoice only
- **Complex tables**: Nested/merged cells may be missed
- **Character encoding**: Non-UTF8 PDFs may have extraction issues

### Future Enhancements
- OCR support for scanned documents
- Machine learning for field extraction
- Multi-language support
- Duplicate detection across invoices
- Workflow/approval system
- Database backend for persistence
- Audit logging

## 📝 AI Usage Notes

### Tools Used
- ChatGPT: FastAPI scaffolding, Pydantic schemas, regex patterns
- GitHub Copilot: React component structure, Tailwind CSS utilities

### AI Contributions
1. **FastAPI setup**: Generated CORS middleware configuration
2. **Regex patterns**: Created date/amount matching patterns (refined for German invoices)
3. **React components**: Scaffolded component structure
4. **Tailwind styling**: Generated utility class combinations

### Corrections Made
- **Issue**: AI-generated regex patterns were too generic
  - **Fix**: Specialized patterns for German invoice keywords (Bestellung, MwSt, etc.)
- **Issue**: Initial amount extraction missed European decimal format (1.234,56)
  - **Fix**: Added `.replace('.',​'').replace(',','.')` for proper parsing
- **Issue**: Validation errors weren't properly categorized
  - **Fix**: Implemented error/warning distinction with severity levels

## 📦 Project Structure

\`\`\`
invoice-qc-service/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── extractor.py         # PDF extraction logic
│   ├── validator.py         # Business rule validation
│   ├── schemas.py           # Pydantic models
│   ├── cli.py               # CLI commands
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Main React component
│   │   ├── index.css                  # Tailwind imports
│   │   └── components/
│   │       ├── Header.jsx             # Page header
│   │       ├── FileUploader.jsx       # File upload widget
│   │       ├── ResultsDisplay.jsx     # Results container
│   │       ├── ValidationResults.jsx  # Validation view
│   │       └── ExtractedDataTable.jsx # Data table view
│   ├── package.json
│   └── vite.config.js
│
└── README.md                # This file
\`\`\`

## 🧪 Sample Test Data

Two sample German B2B invoices are included:
- `sample_pdf_1.pdf`: Single line item invoice
- `sample_pdf_2.pdf`: Multi-line item invoice

Both demonstrate extraction and validation capabilities.

## 📄 License

This is a PoC for demonstration purposes.

---

**Built with:** FastAPI • React • Tailwind CSS • pdfplumber • Pydantic
