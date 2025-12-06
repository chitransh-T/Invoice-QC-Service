

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import List, Optional
from extractor import InvoiceExtractor
from validator import InvoiceValidator
from schemas import InvoiceData, ValidationReport

# Initialize FastAPI app
app = FastAPI(
    title="Invoice QC Service",
    description="Extract and validate invoice PDFs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize extractor and validator
extractor = InvoiceExtractor()
validator = InvoiceValidator()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Invoice QC Service",
        "version": "1.0.0"
    }

@app.post("/api/analyze")
async def analyze_invoice(file: UploadFile = File(...)):
    """
    Analyze a single PDF invoice.
    - Extracts structured data
    - Validates against business rules
    - Returns results
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name
        
        # Extract data from PDF
        extracted_data = extractor.extract(tmp_path)
        
        # Validate extracted data
        validation_result = validator.validate_invoice(extracted_data)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {
            "success": True,
            "extracted": extracted_data,
            "validation": validation_result.dict()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/api/validate-json")
async def validate_json(invoices: List[InvoiceData]):
    """
    Validate a list of invoice JSON objects.
    Returns validation report with per-invoice results and summary.
    """
    try:
        invoice_dicts = [inv.dict() for inv in invoices]
        report = validator.validate(invoice_dicts)
        return report.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@app.post("/api/extract-and-validate")
async def extract_and_validate(files: List[UploadFile] = File(...)):
    """
    Extract and validate multiple PDFs in one request.
    Returns extracted data + validation report.
    """
    try:
        extracted_invoices = []
        temp_paths = []
        
        # Extract all PDFs
        for file in files:
            if not file.filename.endswith('.pdf'):
                continue
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                contents = await file.read()
                tmp_file.write(contents)
                tmp_path = tmp_file.name
                temp_paths.append(tmp_path)
            
            extracted_data = extractor.extract(tmp_path)
            extracted_invoices.append(extracted_data)
        
        # Validate all extracted invoices
        report = validator.validate(extracted_invoices)
        
        # Clean up
        for tmp_path in temp_paths:
            os.unlink(tmp_path)
        
        return {
            "success": True,
            "extracted_count": len(extracted_invoices),
            "extracted": extracted_invoices,
            "validation_report": report.dict()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
