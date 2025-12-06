# HTTP API Usage Guide

The Invoice QC Service provides REST API endpoints for extracting and validating invoices. The API runs on `http://localhost:8000` by default.

## Prerequisites

1. **Start the backend server:**
   ```powershell
   cd backend
   venv\Scripts\activate
   python -m uvicorn main:app --reload
   ```

   The API will be available at: `http://localhost:8000`

2. **API Documentation:**
   Once the server is running, visit:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

## Available Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "Invoice QC Service",
  "version": "1.0.0"
}
```

---

### 2. Analyze Single Invoice (Extract + Validate)
**POST** `/api/analyze`

Upload a single PDF invoice, extract data, and validate it.

**Request:**
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Body:** Form data with `file` field containing the PDF

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@/path/to/invoice.pdf"
```

**Using Python (requests):**
```python
import requests

url = "http://localhost:8000/api/analyze"
with open("invoice.pdf", "rb") as f:
    files = {"file": ("invoice.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)
    
result = response.json()
print(result)
```

**Using JavaScript (fetch):**
```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);

const response = await fetch("http://localhost:8000/api/analyze", {
  method: "POST",
  body: formData,
});

const result = await response.json();
console.log(result);
```

**Response:**
```json
{
  "success": true,
  "extracted": {
    "invoice_number": "AUFNR34343",
    "invoice_date": "2024-01-15",
    "due_date": "2024-01-29",
    "seller_name": "ABC Corporation",
    "buyer_name": "Beispielname Unternehmen",
    "currency": "EUR",
    "net_total": 1000.0,
    "tax_amount": 190.0,
    "gross_total": 1190.0,
    "tax_percentage": 19.0,
    "line_items": [...],
    "status": "pending"
  },
  "validation": {
    "invoice_number": "AUFNR34343",
    "is_valid": true,
    "errors": [],
    "warnings": []
  }
}
```

---

### 3. Validate JSON Invoice Data
**POST** `/api/validate-json`

Validate already-extracted invoice data (JSON format) without processing PDFs.

**Request:**
- **Method:** POST
- **Content-Type:** `application/json`
- **Body:** Array of invoice objects

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/validate-json" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "invoice_number": "INV-001",
      "invoice_date": "2024-01-15",
      "seller_name": "Company A",
      "buyer_name": "Company B",
      "net_total": 1000.0,
      "tax_amount": 190.0,
      "gross_total": 1190.0,
      "currency": "EUR"
    }
  ]'
```

**Using Python (requests):**
```python
import requests

url = "http://localhost:8000/api/validate-json"
invoices = [
    {
        "invoice_number": "INV-001",
        "invoice_date": "2024-01-15",
        "seller_name": "Company A",
        "buyer_name": "Company B",
        "net_total": 1000.0,
        "tax_amount": 190.0,
        "gross_total": 1190.0,
        "currency": "EUR"
    }
]

response = requests.post(url, json=invoices)
report = response.json()
print(report)
```

**Using JavaScript (fetch):**
```javascript
const invoices = [
  {
    invoice_number: "INV-001",
    invoice_date: "2024-01-15",
    seller_name: "Company A",
    buyer_name: "Company B",
    net_total: 1000.0,
    tax_amount: 190.0,
    gross_total: 1190.0,
    currency: "EUR"
  }
];

const response = await fetch("http://localhost:8000/api/validate-json", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(invoices),
});

const report = await response.json();
console.log(report);
```

**Response:**
```json
{
  "total_invoices": 1,
  "valid_invoices": 1,
  "invalid_invoices": 0,
  "error_summary": {},
  "detailed_results": [
    {
      "invoice_number": "INV-001",
      "is_valid": true,
      "errors": [],
      "warnings": []
    }
  ]
}
```

---

### 4. Extract and Validate Multiple PDFs
**POST** `/api/extract-and-validate`

Upload multiple PDF invoices, extract data from all, and get a validation report.

**Request:**
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Body:** Form data with multiple `files` (array)

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/extract-and-validate" \
  -F "files=@/path/to/invoice1.pdf" \
  -F "files=@/path/to/invoice2.pdf" \
  -F "files=@/path/to/invoice3.pdf"
```

**Using Python (requests):**
```python
import requests

url = "http://localhost:8000/api/extract-and-validate"
files = [
    ("files", ("invoice1.pdf", open("invoice1.pdf", "rb"), "application/pdf")),
    ("files", ("invoice2.pdf", open("invoice2.pdf", "rb"), "application/pdf")),
    ("files", ("invoice3.pdf", open("invoice3.pdf", "rb"), "application/pdf")),
]

response = requests.post(url, files=files)
result = response.json()
print(result)
```

**Using JavaScript (fetch):**
```javascript
const formData = new FormData();
formData.append("files", file1);
formData.append("files", file2);
formData.append("files", file3);

const response = await fetch("http://localhost:8000/api/extract-and-validate", {
  method: "POST",
  body: formData,
});

const result = await response.json();
console.log(result);
```

**Response:**
```json
{
  "success": true,
  "extracted_count": 3,
  "extracted": [
    {
      "invoice_number": "INV-001",
      "invoice_date": "2024-01-15",
      ...
    },
    {
      "invoice_number": "INV-002",
      ...
    },
    {
      "invoice_number": "INV-003",
      ...
    }
  ],
  "validation_report": {
    "total_invoices": 3,
    "valid_invoices": 2,
    "invalid_invoices": 1,
    "error_summary": {
      "invoice_number: Invoice number is missing": 1
    },
    "detailed_results": [...]
  }
}
```

---

## Complete Python Example

Here's a complete Python script to process invoices via the API:

```python
import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def analyze_single_invoice(pdf_path):
    """Analyze a single invoice PDF."""
    url = f"{BASE_URL}/api/analyze"
    
    with open(pdf_path, "rb") as f:
        files = {"file": (Path(pdf_path).name, f, "application/pdf")}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def validate_json_invoices(invoices_data):
    """Validate invoice data from JSON."""
    url = f"{BASE_URL}/api/validate-json"
    
    response = requests.post(url, json=invoices_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def process_multiple_pdfs(pdf_paths):
    """Process multiple PDFs at once."""
    url = f"{BASE_URL}/api/extract-and-validate"
    
    files = []
    for pdf_path in pdf_paths:
        files.append(
            ("files", (Path(pdf_path).name, open(pdf_path, "rb"), "application/pdf"))
        )
    
    response = requests.post(url, files=files)
    
    # Close file handles
    for _, (_, file_handle, _) in files:
        file_handle.close()
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    # Example 1: Analyze single invoice
    result = analyze_single_invoice("invoice.pdf")
    print("Single Invoice Analysis:")
    print(json.dumps(result, indent=2))
    
    # Example 2: Validate JSON data
    invoices = [
        {
            "invoice_number": "INV-001",
            "invoice_date": "2024-01-15",
            "seller_name": "Company A",
            "buyer_name": "Company B",
            "net_total": 1000.0,
            "tax_amount": 190.0,
            "gross_total": 1190.0,
        }
    ]
    report = validate_json_invoices(invoices)
    print("\nValidation Report:")
    print(json.dumps(report, indent=2))
    
    # Example 3: Process multiple PDFs
    pdf_files = ["invoice1.pdf", "invoice2.pdf", "invoice3.pdf"]
    batch_result = process_multiple_pdfs(pdf_files)
    print("\nBatch Processing Result:")
    print(json.dumps(batch_result, indent=2))
```

---

## Complete JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch'); // or use built-in fetch in Node 18+

const BASE_URL = 'http://localhost:8000';

async function analyzeSingleInvoice(pdfPath) {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(pdfPath));
  
  const response = await fetch(`${BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status} - ${await response.text()}`);
  }
  
  return await response.json();
}

async function validateJsonInvoices(invoices) {
  const response = await fetch(`${BASE_URL}/api/validate-json`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(invoices),
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status} - ${await response.text()}`);
  }
  
  return await response.json();
}

async function processMultiplePDFs(pdfPaths) {
  const formData = new FormData();
  pdfPaths.forEach(path => {
    formData.append('files', fs.createReadStream(path));
  });
  
  const response = await fetch(`${BASE_URL}/api/extract-and-validate`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status} - ${await response.text()}`);
  }
  
  return await response.json();
}

// Example usage
(async () => {
  try {
    // Example 1: Analyze single invoice
    const result = await analyzeSingleInvoice('invoice.pdf');
    console.log('Single Invoice Analysis:', JSON.stringify(result, null, 2));
    
    // Example 2: Validate JSON
    const invoices = [{
      invoice_number: 'INV-001',
      invoice_date: '2024-01-15',
      seller_name: 'Company A',
      buyer_name: 'Company B',
      net_total: 1000.0,
      tax_amount: 190.0,
      gross_total: 1190.0,
    }];
    const report = await validateJsonInvoices(invoices);
    console.log('Validation Report:', JSON.stringify(report, null, 2));
    
    // Example 3: Process multiple PDFs
    const batchResult = await processMultiplePDFs([
      'invoice1.pdf',
      'invoice2.pdf',
      'invoice3.pdf',
    ]);
    console.log('Batch Result:', JSON.stringify(batchResult, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- **200 OK** - Success
- **400 Bad Request** - Invalid input (e.g., non-PDF file)
- **500 Internal Server Error** - Processing error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

**Example Error Handling (Python):**
```python
try:
    response = requests.post(url, files=files)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    result = response.json()
except requests.exceptions.HTTPError as e:
    error_detail = e.response.json().get("detail", "Unknown error")
    print(f"API Error: {error_detail}")
```

---

## Testing with Postman

1. **Import Collection:**
   - Create a new request
   - Set method to POST
   - URL: `http://localhost:8000/api/analyze`
   - Go to Body tab → Select "form-data"
   - Add key: `file` (type: File)
   - Select a PDF file
   - Click Send

2. **For Multiple Files:**
   - URL: `http://localhost:8000/api/extract-and-validate`
   - Body → form-data
   - Add multiple `files` keys, each with a PDF file

---

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Next.js/React)
- `http://localhost:8080` (Alternative port)

If you need to add more origins, edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://your-domain.com"],
    ...
)
```

---

## Rate Limiting & Performance

- No rate limiting is currently implemented
- Processing time depends on PDF size and complexity
- For large batches, consider using the batch endpoint or processing in chunks

---

## Next Steps

- Visit `http://localhost:8000/docs` for interactive API documentation
- Use the web UI at `http://localhost:5173` for a visual interface
- Check the CLI guide (`CLI_USAGE.md`) for command-line processing

