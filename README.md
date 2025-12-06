
A complete B2B invoice extraction and quality control system with FastAPI backend and React frontend.

---

## 📋 Overview

### What You Built

This project is a **complete invoice quality control (QC) system** that automates the extraction and validation of invoice data from PDF documents. It's designed for B2B invoice processing workflows, with a focus on German invoice formats.

**Core Capabilities:**
- **PDF Data Extraction**: Automatically extracts structured data (invoice numbers, dates, amounts, parties, line items) from PDF invoices using regex pattern matching
- **Business Rule Validation**: Validates extracted data against completeness, format, and business logic rules
- **Multiple Interfaces**: Provides CLI, REST API, and web UI for different use cases
- **Batch Processing**: Supports processing multiple invoices simultaneously

### Which Parts I Completed

✅ **Extraction Module** (`backend/extractor.py`)
- PDF text extraction using pdfplumber
- Regex-based field extraction (invoice number, dates, amounts, parties)
- Line item extraction from invoice tables
- Support for German invoice formats and European number formats

✅ **Validation Engine** (`backend/validator.py`)
- Completeness validation (required fields)
- Format validation (dates, currencies)
- Business rule validation (totals, calculations)
- Error/warning categorization with detailed messages

✅ **CLI Tool** (`backend/cli.py`)
- `extract`: Extract data from PDFs to JSON
- `validate-cmd`: Validate extracted JSON data
- `full-run`: Complete extraction + validation pipeline
- Terminal output with progress and summaries

✅ **REST API** (`backend/main.py`)
- FastAPI-based RESTful API
- 4 endpoints: health check, analyze single invoice, validate JSON, batch processing
- CORS enabled for frontend integration
- Interactive API documentation (Swagger/ReDoc)

✅ **Frontend UI** (`frontend/`)
- React-based web interface
- File upload with drag-and-drop
- Real-time validation results display
- Tabbed interface for validation results and extracted data
- Modern UI with Tailwind CSS

---

## 📊 Schema & Validation Design

### List of Fields (with Short Descriptions)

#### Invoice-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `invoice_number` | string | Unique invoice identifier (e.g., "AUFNR34343", "INV-001") |
| `invoice_date` | string (YYYY-MM-DD) | Date when invoice was issued |
| `due_date` | string (YYYY-MM-DD) | Payment due date (auto-calculated if not found) |
| `seller_name` | string | Vendor/supplier company name |
| `seller_address` | string | Vendor's full address |
| `buyer_name` | string | Customer/buyer company name |
| `buyer_address` | string | Customer's full address |
| `currency` | string | Transaction currency code (EUR, USD, GBP, etc.) |
| `net_total` | float | Total amount before tax |
| `tax_amount` | float | Tax/VAT amount |
| `gross_total` | float | Total amount including tax |
| `tax_percentage` | float | Tax rate percentage (default: 19.0 for German invoices) |
| `payment_terms` | string | Payment conditions/terms |
| `status` | string | Processing status (default: "pending") |

#### Line Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Product or service description |
| `quantity` | float | Number of units |
| `unit_price` | float | Price per unit |
| `line_total` | float | Total for this line item (quantity × unit_price) |

### List of Validation Rules (with Rationale)

#### Completeness Rules (Must Have)

| Rule | Rationale |
|------|-----------|
| Invoice number must not be empty | Required for invoice identification and tracking |
| Invoice date must be present and valid | Essential for payment terms and accounting |
| Seller name must not be empty | Required for vendor identification |
| Buyer name must not be empty | Required for customer identification |

#### Format Validation Rules

| Rule | Rationale |
|------|-----------|
| Invoice date must be in valid date format (supports: DD.MM.YYYY, DD/MM/YYYY, YYYY-MM-DD) | Ensures dates can be parsed and used in calculations |
| Currency must be in known set (EUR, USD, GBP, CHF, CNY, JPY, INR) | Prevents invalid currency codes that could cause processing errors |
| Due date must be on or after invoice date | Logical constraint - payment due date cannot be before invoice date |
| Invoice date should not be more than 10 years old | Flags potentially outdated or incorrect dates |

#### Business Logic Rules

| Rule | Rationale |
|------|-----------|
| Gross total must be greater than 0 | Invoices must have a positive amount |
| `gross_total` must equal `net_total + tax_amount` (tolerance: ±0.01) | Ensures mathematical correctness of invoice calculations |
| Line items total should match net total (tolerance: ±0.01) | Verifies that line item sums match the invoice summary |
| Tax amount should match `net_total × tax_percentage` | Validates tax calculation accuracy |

#### Anomaly Detection Rules

| Rule | Rationale |
|------|-----------|
| Flag invoices with dates in the future | Catches data entry errors or test data |
| Flag unknown currencies | Alerts to potential data quality issues |
| Flag mismatched totals | Identifies calculation errors or extraction issues |

---

## 🏗️ Architecture

### Folder Structure

```
Invoice QC Service/
├── backend/                          # Python backend
│   ├── main.py                       # FastAPI REST API server
│   ├── extractor.py                  # PDF extraction logic
│   ├── validator.py                  # Business rule validation engine
│   ├── schemas.py                    # Pydantic data models
│   ├── cli.py                        # Command-line interface
│   ├── requirements.txt              # Python dependencies
│   └── venv/                         # Virtual environment (gitignored)
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── App.jsx                   # Main React application component
│   │   ├── main.jsx                  # React entry point
│   │   ├── index.css                 # Tailwind CSS imports
│   │   └── components/
│   │       ├── Header.jsx            # Page header component
│   │       ├── FileUploader.jsx      # PDF file upload widget
│   │       ├── ResultsDisplay.jsx    # Results container with tabs
│   │       ├── ValidationResults.jsx # Validation errors/warnings display
│   │       └── ExtractedDataTable.jsx # Extracted data table view
│   ├── package.json                  # Node.js dependencies
│   ├── vite.config.js                # Vite build configuration
│   └── tailwind.config.js            # Tailwind CSS configuration
│
├── pdfs/                             # Sample PDF invoices (gitignored)
├── public/                           # Static assets
├── lib/                              # Shared utilities
│   └── utils.ts                      # TypeScript utility functions
├── styles/                           # Global styles
│   └── globals.css
├── .gitignore                        # Git ignore rules
├── README.md                         # This file
├── API_USAGE.md                      # Detailed API documentation
├── CLI_USAGE.md                      # Detailed CLI documentation
└── QUICKSTART.md                     # Quick start guide
```

### Short Explanation of Components

#### Extraction Pipeline (`backend/extractor.py`)

**Purpose**: Converts PDF invoices into structured JSON data.

**How it works:**
1. **PDF Text Extraction**: Uses `pdfplumber` library to extract raw text from all pages of the PDF
2. **Pattern Matching**: Applies regex patterns to find specific fields:
   - Invoice numbers: Matches patterns like "AUFNR", "Bestellung", "Invoice #"
   - Dates: Supports multiple formats (DD.MM.YYYY, YYYY-MM-DD, etc.)
   - Amounts: Extracts currency amounts, handles European format (1.234,56)
   - Parties: Identifies seller/buyer using keywords and text position
3. **Text Heuristics**: Uses context clues (keywords like "Lieferant", "Kunde") to identify seller vs buyer
4. **Line Item Extraction**: Parses invoice tables to extract quantity, description, unit price, and totals
5. **Data Normalization**: Converts dates to ISO format (YYYY-MM-DD), normalizes amounts to floats
6. **Default Values**: Applies sensible defaults (e.g., 19% tax for German invoices, EUR currency)

**Key Methods:**
- `extract(pdf_path)`: Main entry point - extracts data from PDF file
- `_parse_invoice_text(text)`: Core parsing logic
- `_find_pattern(text, patterns)`: Regex pattern matching
- `_extract_amounts(text)`: Amount extraction with format handling

#### Validation Core (`backend/validator.py`)

**Purpose**: Validates extracted invoice data against business rules.

**How it works:**
1. **Rule Categories**: Organizes validation into:
   - Completeness rules (required fields)
   - Format rules (date formats, currency codes)
   - Business rules (totals, calculations)
   - Anomaly detection (future dates, mismatches)
2. **Error Classification**: Categorizes issues as:
   - **Errors**: Critical issues that make invoice invalid (missing required fields, calculation errors)
   - **Warnings**: Non-critical issues (unknown currency, old dates)
3. **Per-Invoice Validation**: `validate_invoice()` validates a single invoice
4. **Batch Validation**: `validate()` processes multiple invoices and generates aggregated report
5. **Tolerance Handling**: Uses configurable tolerance (default ±0.01) for floating-point comparisons

**Key Methods:**
- `validate_invoice(invoice)`: Validates single invoice, returns ValidationResult
- `validate(invoices)`: Validates list of invoices, returns ValidationReport
- Individual rule checkers (completeness, format, business logic)

#### CLI (`backend/cli.py`)

**Purpose**: Command-line interface for batch processing invoices.

**How it works:**
1. **Click Framework**: Uses Python `click` library for command-line argument parsing
2. **Three Commands**:
   - `extract`: Extracts data from all PDFs in a directory, saves to JSON
   - `validate-cmd`: Validates previously extracted JSON data
   - `full-run`: Complete pipeline (extract + validate) in one command
3. **Progress Feedback**: Shows file-by-file progress during processing
4. **Summary Output**: Displays validation summary in terminal
5. **JSON Reports**: Saves detailed validation reports to JSON files

**Usage Flow:**
```bash
# Option 1: Full pipeline (recommended)
python cli.py full-run --pdf-dir ./pdfs --report report.json

# Option 2: Two-step process
python cli.py extract --pdf-dir ./pdfs --output data.json
python cli.py validate-cmd --input data.json --report report.json
```

#### API (`backend/main.py`)

**Purpose**: RESTful API for programmatic access to extraction and validation.

**How it works:**
1. **FastAPI Framework**: Modern Python web framework with automatic OpenAPI documentation
2. **CORS Middleware**: Enables cross-origin requests from frontend
3. **File Upload Handling**: Accepts PDF files via multipart/form-data
4. **Temporary File Management**: Creates temporary files for uploaded PDFs, cleans up after processing
5. **Error Handling**: Returns appropriate HTTP status codes and error messages

**Endpoints:**
- `GET /health`: Health check endpoint
- `POST /api/analyze`: Single PDF upload, extract + validate
- `POST /api/validate-json`: Validate pre-extracted JSON data
- `POST /api/extract-and-validate`: Batch process multiple PDFs

**Response Format**: JSON with extracted data and validation results

#### Frontend (`frontend/`)

**Purpose**: User-friendly web interface for invoice processing.

**How it works:**
1. **React Framework**: Component-based UI using React 18
2. **Vite Build Tool**: Fast development server and optimized production builds
3. **Tailwind CSS**: Utility-first CSS framework for styling
4. **Component Architecture**:
   - `App.jsx`: Main application state management
   - `FileUploader.jsx`: Handles PDF file selection and upload
   - `ResultsDisplay.jsx`: Container for results with tab switching
   - `ValidationResults.jsx`: Displays errors and warnings
   - `ExtractedDataTable.jsx`: Shows extracted data in table format
5. **API Integration**: Uses `fetch` API to communicate with backend
6. **Real-time Feedback**: Shows loading states and error messages

**User Flow:**
1. User clicks "Choose PDF" button
2. File input opens, user selects PDF
3. File is uploaded to `/api/analyze` endpoint
4. Loading spinner displays
5. Results appear in two tabs: Validation Results and Extracted Data

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Invoice QC Service                        │
└─────────────────────────────────────────────────────────────────┘

PDF Files
    │
    ├─────────────────────────────────────────────────────────────┐
    │                                                             │
    ▼                                                             ▼
┌──────────────┐                                         ┌──────────────┐
│   CLI Tool   │                                         │  REST API    │
│  (cli.py)    │                                         │  (main.py)   │
└──────┬───────┘                                         └──────┬───────┘
       │                                                        │
       │                                                        │
       ▼                                                        ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Extraction Module                             │
│                    (extractor.py)                                │
│                                                                   │
│  PDF → pdfplumber → Raw Text → Regex Patterns → Structured JSON  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Extracted JSON Data  │
                    └───────────┬───────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Validation Engine                                │
│                  (validator.py)                                   │
│                                                                   │
│  JSON → Completeness Rules → Format Rules → Business Rules       │
│       → Error/Warning Classification → Validation Report         │
└──────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ JSON Report │ │  API Response│ │  UI Display │
        │  (CLI)      │ │  (REST API)  │ │  (Frontend) │
        └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 🚀 Setup & Installation

### Python Version

**Required**: Python 3.9 or higher

Check your Python version:
```bash
python --version
# Should show: Python 3.9.x or higher
```

### How to Create Virtual Environment and Install Dependencies

#### Step 1: Navigate to Project Directory
```bash
cd "Invoice QC Service"
```

#### Step 2: Create Virtual Environment
```bash
# On Windows (PowerShell)
python -m venv backend\venv

# On Linux/Mac
python -m venv backend/venv
```

#### Step 3: Activate Virtual Environment
```bash
# On Windows (PowerShell)
backend\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
backend\venv\Scripts\activate.bat

# On Linux/Mac
source backend/venv/bin/activate
```

**Note**: After activation, your terminal prompt should show `(venv)`.

#### Step 4: Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```

This installs:
- `fastapi` - Web framework for REST API
- `uvicorn` - ASGI server
- `pdfplumber` - PDF text extraction
- `pydantic` - Data validation and settings
- `click` - CLI framework
- `python-multipart` - File upload support
- `python-dotenv` - Environment variable management

### How to Run CLI

#### Prerequisites
- Virtual environment activated
- Dependencies installed

#### Command Examples

**1. Extract data from PDFs:**
```bash
# From project root directory
cd backend
python cli.py extract --pdf-dir "../pdfs" --output "extracted.json"
```

**2. Validate extracted data:**
```bash
python cli.py validate-cmd --input "extracted.json" --report "report.json"
```

**3. Full pipeline (extract + validate):**
```bash
python cli.py full-run --pdf-dir "../pdfs" --report "validation_report.json"
```

**Note**: Replace `"../pdfs"` with the actual path to your PDF directory.

### How to Run API

#### Step 1: Activate Virtual Environment
```bash
cd backend
backend\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source backend/venv/bin/activate    # Linux/Mac
```

#### Step 2: Start the Server
```bash
# From backend directory
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or from project root
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Flags explained:**
- `--reload`: Auto-reload on code changes (development mode)
- `--host 0.0.0.0`: Listen on all network interfaces
- `--port 8000`: Use port 8000

#### Step 3: Verify API is Running
Open your browser and visit:
- API Health Check: `http://localhost:8000/health`
- Interactive API Docs: `http://localhost:8000/docs` (Swagger UI)
- Alternative Docs: `http://localhost:8000/redoc` (ReDoc)

You should see JSON responses or API documentation.

### How to Run Frontend

#### Prerequisites
- Node.js 16+ installed
- npm or pnpm package manager

#### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

#### Step 2: Install Dependencies
```bash
npm install
# or
pnpm install
```

This installs:
- React and React DOM
- Vite (build tool)
- Tailwind CSS
- PostCSS and Autoprefixer

#### Step 3: Start Development Server
```bash
npm run dev
# or
pnpm dev
```

#### Step 4: Access the UI
Open your browser and visit: `http://localhost:5173`

**Note**: Make sure the backend API is running on `http://localhost:8000` for the frontend to work properly.

---

## 💻 Usage


#### Full Run (Recommended)
```bash
# Complete extraction + validation in one command
python cli.py full-run --pdf-dir "../pdfs" --report "validation_report.json" 
```

**Output**: Terminal shows progress and summary, JSON report saved to file.

### Example HTTP Calls

#### Using cURL

**1. Health Check:**
```bash
curl http://localhost:8000/health
```

**2. Analyze Single Invoice:**
```bash
curl.exe -X POST "http://localhost:8000/api/analyze" -F "file=@pdfs\sample_pdf_1.pdf"  
```

**3. Validate JSON Data:**
```bash
curl -X POST http://localhost:8000/api/validate-json \
  -H "Content-Type: application/json" \
  -d '[{
    "invoice_number": "INV-001",
    "invoice_date": "2024-01-15",
    "seller_name": "Company A",
    "buyer_name": "Company B",
    "net_total": 1000.0,
    "tax_amount": 190.0,
    "gross_total": 1190.0,
    "currency": "EUR"
  }]'
```

**4. Batch Process Multiple PDFs:**
```bash
curl.exe -X POST "http://localhost:8000/api/extract-and-validate" -F "files=@pdfs\sample_pdf_1.pdf" -F "files=@pdfs\sample_pdf_2.pdf" -F "files=@pdfs\sample_pdf_3.pdf" | jq . 
```


### Frontend Usage

**How to Operate the Web UI:**

1. **Start the Application:**
   - Ensure backend API is running on `http://localhost:8000`
   - Start frontend: `cd frontend && npm run dev`
   - Open browser to `http://localhost:5173`

2. **Upload an Invoice:**
   - Click the "Choose PDF" button
   - Select a PDF invoice file from your computer
   - Wait for processing (loading spinner will appear)

3. **View Results:**
   - **Validation Results Tab**: Shows errors and warnings with field-level details
   - **Extracted Data Tab**: Displays all extracted fields in a structured table
   - Green checkmarks indicate valid fields
   - Red X marks indicate errors
   - Yellow warnings indicate non-critical issues

4. **Process Another Invoice:**
   - Upload a new PDF to replace the current results

**Note**: The UI automatically connects to the backend API. If you see connection errors, verify the API is running.

---

## 🤖 AI Usage Notes

### Tools Used

- **ChatGPT**: Used for initial project scaffolding, FastAPI setup, Pydantic schema generation, and regex pattern development
- **GitHub Copilot**: Assisted with React component structure, Tailwind CSS utility class selection, and code completion

### AI Contributions

1. **FastAPI Setup**
   - Generated initial FastAPI application structure
   - Created CORS middleware configuration for frontend integration
   - Suggested endpoint structure and response formats

2. **Regex Patterns**
   - Initial patterns for date, amount, and invoice number extraction
   - **Refinement**: Patterns were later specialized for German invoice keywords (e.g., "Bestellung", "MwSt", "AUFNR")

3. **React Components**
   - Scaffolded component structure and file organization
   - Suggested component props and state management patterns
   - Generated initial JSX templates

4. **Tailwind CSS Styling**
   - Suggested utility class combinations for layouts
   - Generated color schemes and spacing configurations

### Corrections Made

1. **Issue**: AI-generated regex patterns were too generic
   - **Problem**: Initial patterns didn't account for German invoice terminology
   - **Fix**: Specialized patterns for German keywords like "Bestellung", "Rechnungsnummer", "Lieferant", "Kunde"
   - **Result**: Improved extraction accuracy for German B2B invoices

2. **Issue**: Initial amount extraction missed European decimal format
   - **Problem**: European format uses dots for thousands and commas for decimals (e.g., 1.234,56)
   - **Fix**: Added `.replace('.', '').replace(',', '.')` transformation before float parsing
   - **Result**: Correctly parses amounts like "1.234,56 EUR" as 1234.56

3. **Issue**: Validation errors weren't properly categorized
   - **Problem**: All issues were treated as errors, no distinction between critical and non-critical
   - **Fix**: Implemented error/warning distinction with severity levels
   - **Result**: Better user experience with clear error vs warning separation

---

## ⚠️ Assumptions & Limitations

### What You Intentionally Simplified (Due to Time)

1. **Regex-Based Extraction**
   - **Simplification**: Used regex patterns instead of OCR or ML-based extraction
   - **Rationale**: Faster to implement, works well for structured PDFs with extractable text
   - **Trade-off**: Doesn't work for scanned/image-based PDFs without OCR

2. **Single Tax Rate Assumption**
   - **Simplification**: Assumes one tax rate per invoice (default 19% for German invoices)
   - **Rationale**: Most B2B invoices use a single rate; multi-rate support adds complexity
   - **Trade-off**: Complex invoices with multiple tax rates may not validate correctly

3. **German Invoice Focus**
   - **Simplification**: Patterns optimized for German invoice formats and terminology
   - **Rationale**: Focused scope for PoC; easier to achieve high accuracy for one format
   - **Trade-off**: May not work well for invoices from other countries without pattern updates

4. **Limited Line Item Extraction**
   - **Simplification**: Basic table parsing; doesn't handle complex nested/merged cells
   - **Rationale**: Simple regex-based extraction for common table structures
   - **Trade-off**: Complex invoice tables with merged cells may miss some line items

5. **No Database Persistence**
   - **Simplification**: All processing is stateless; no database for storing invoices
   - **Rationale**: PoC focuses on extraction/validation logic, not data persistence
   - **Trade-off**: Results are not saved between sessions

6. **No Authentication/Authorization**
   - **Simplification**: API has no authentication or user management
   - **Rationale**: PoC focuses on core functionality
   - **Trade-off**: Not production-ready for multi-user scenarios


 ## 🧪 Sample Test Data

Two sample German B2B invoices are included:
- `sample_pdf_1.pdf`: Single line item invoice
- `sample_pdf_2.pdf`: Multi-line item invoice

Both demonstrate extraction and validation capabilities.

## 📄 License

This is a PoC for demonstration purposes.

---

**Built with:** FastAPI • React • Tailwind CSS • pdfplumber • Pydantic

**Video link:**

---> https://drive.google.com/drive/u/1/folders/10SuLVRT-kTB6punZ9vilkxs6wWzPGslP