# Invoice QC Service - Quick Start Guide

This is a complete proof-of-concept for invoice extraction and validation. The system consists of a FastAPI backend and a React/Vite frontend.

## Architecture

\`\`\`
Frontend (React/Vite)         Backend (FastAPI)
    ↓                             ↓
Upload PDF ----API-call--→ Process PDF
   ↓                        Extract Data
Display Results ←----JSON--- Validate Rules
\`\`\`

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- pip (Python package manager)
- npm or pnpm

## Backend Setup (One-time)

### Step 1: Navigate to Backend

\`\`\`bash
cd backend
\`\`\`

### Step 2: Create Virtual Environment

**macOS/Linux:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

**Windows:**
\`\`\`bash
python -m venv venv
venv\Scripts\activate
\`\`\`

### Step 3: Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

This installs:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **pdfplumber** - PDF extraction

## Running the System

### Terminal 1: Start Backend Server

\`\`\`bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload
\`\`\`

You should see:
\`\`\`
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
\`\`\`

**Keep this terminal open!**

### Terminal 2: Start Frontend

The frontend runs in v0 preview automatically, or locally:

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Then open: `http://localhost:5173`

## Testing the System


1. Select one of the sample PDFs provided
2. The system will:
   - Extract invoice data (numbers, dates, amounts, parties)
   - Run validation rules (completeness, format, business logic)
   - Display results with errors and extracted data

## What Gets Validated

**Completeness Rules:**
- ✓ Invoice number present
- ✓ Invoice date present
- ✓ Seller name present
- ✓ Buyer name present

**Format Rules:**
- ✓ Valid date format
- ✓ Date is not in future
- ✓ Known currency code
- ✓ Due date after invoice date

**Business Logic Rules:**
- ✓ Gross total = Net total + Tax amount (±0.01 tolerance)
- ✓ All amounts are positive
- ✓ Line items total matches net total

**Anomaly Detection:**
- ✓ Detects old invoices (>10 years)
- ✓ Detects unknown currencies
- ✓ Detects line item mismatches

## Backend API Endpoints

### POST /api/analyze
Analyzes a single PDF invoice.

**Request:**
\`\`\`
Content-Type: multipart/form-data
file: <PDF file>
\`\`\`

**Response:**
\`\`\`json
{
  "success": true,
  "extracted": { ...invoice data... },
  "validation": {
    "is_valid": true/false,
    "invoice_number": "INV-001",
    "errors": [...],
    "warnings": [...]
  }
}
\`\`\`

### GET /health
Health check endpoint.

**Response:**
\`\`\`json
{
  "status": "ok",
  "service": "Invoice QC Service",
  "version": "1.0.0"
}
\`\`\`

## Troubleshooting

### "Failed to fetch" Error
**Cause:** Backend is not running or API URL is wrong

**Solution:**
1. Ensure backend terminal shows: `Uvicorn running on http://127.0.0.1:8000`
2. Check environment variable: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Restart backend: `python -m uvicorn main:app --reload`

### "Only PDF files are supported"
**Cause:** File is not a PDF

**Solution:** Select a valid PDF file

### "Error processing file"
**Cause:** PDF structure not recognized or extraction failed

**Solution:**
1. Verify PDF is not corrupted
2. Check backend logs for details
3. Try a different PDF

### Backend won't start
**Cause:** Missing dependencies or port 8000 in use

**Solution:**
\`\`\`bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use different port
python -m uvicorn main:app --reload --port 8001
\`\`\`

## Project Structure

\`\`\`
.
├── backend/
│   ├── main.py              # FastAPI app with endpoints
│   ├── extractor.py         # PDF extraction logic
│   ├── validator.py         # Validation rules
│   ├── schemas.py           # Pydantic models
│   ├── requirements.txt      # Python dependencies
│   └── venv/                # Virtual environment (created after setup)
│
└── frontend/
    └── src/
        ├── App.jsx          # Main React component
        ├── main.jsx         # Entry point
        └── components/      # React components
└── components/
    ├── FileUploader.tsx     # File upload component
    ├── ResultsDisplay.tsx   # Results viewer
    ├── ValidationResults.tsx # Validation details
    ├── ExtractedDataTable.tsx # Data table
    └── Header.tsx           # Header component
\`\`\`

## Performance Notes

- **PDF Extraction:** ~1-2 seconds for typical invoices
- **Validation:** <100ms for each invoice
- **Max File Size:** Limited by form data (default 10MB)

## Production Deployment

For production:

1. **Backend:** Use Gunicorn with Uvicorn workers
   \`\`\`bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   \`\`\`

2. **Frontend:** Build and deploy
   \`\`\`bash
   cd frontend
   npm run build
   \`\`\`

3. **Environment:** Set API URL to production backend URL in frontend components

## Sample PDFs

Two sample German B2B invoices are provided in `user_read_only_context/text_attachments/`:
- `sample_pdf_1-*.pdf` - Example 1
- `sample_pdf_2-*.pdf` - Example 2

These demonstrate invoice extraction and validation.

## Support

For issues:
1. Check backend logs (Terminal 1)
2. Check browser console (F12)
3. Verify both services are running
4. Restart backend with: `python -m uvicorn main:app --reload`
