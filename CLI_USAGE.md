# CLI Usage Guide

The Invoice QC CLI tool provides three commands for processing invoices from the command line.

## Prerequisites

1. Make sure you're in the backend directory with the virtual environment activated:
   ```powershell
   cd backend
   venv\Scripts\activate
   ```

## Command 1: Full Run (Extract + Validate)

This command extracts data from PDFs and validates them in one step - **recommended for most use cases**.

### Usage:
```powershell
python cli.py full-run --pdf-dir "path/to/pdf/folder" --report "output_report.json"
```

### Example:
```powershell
# Validate all PDFs in a folder
python cli.py full-run --pdf-dir "C:\Users\HP\Desktop\invoices" --report "validation_report.json"
```

### What it does:
1. Scans the specified directory for all PDF files
2. Extracts structured data from each PDF
3. Validates all invoices against business rules
4. Generates a comprehensive validation report
5. Displays a summary in the terminal

### Output:
- Terminal shows progress and summary
- JSON report file with detailed validation results

---

## Command 2: Extract Only

Extract invoice data from PDFs without validation (saves to JSON).

### Usage:
```powershell
python cli.py extract --pdf-dir "path/to/pdf/folder" --output "extracted_data.json"
```

### Example:
```powershell
python cli.py extract --pdf-dir "C:\Users\HP\Desktop\invoices" --output "invoices.json"
```

### What it does:
- Extracts data from all PDFs in the directory
- Saves extracted data to a JSON file
- Does NOT validate the data

---

## Command 3: Validate Only

Validate previously extracted invoice data from a JSON file.

### Usage:
```powershell
python cli.py validate-cmd --input "extracted_data.json" --report "validation_report.json"
```

### Example:
```powershell
# First extract (if not done already)
python cli.py extract --pdf-dir "C:\Users\HP\Desktop\invoices" --output "invoices.json"

# Then validate
python cli.py validate-cmd --input "invoices.json" --report "report.json"
```

### What it does:
- Reads invoice data from a JSON file
- Validates against all business rules
- Generates a validation report
- Shows summary in terminal

---

## Example Workflow

### Complete validation workflow:

```powershell
# Step 1: Navigate to backend and activate venv
cd backend
venv\Scripts\activate

# Step 2: Run full validation (recommended)
python cli.py full-run --pdf-dir "C:\Users\HP\Desktop\test_invoices" --report "report.json"
```

### Two-step workflow (if you want to inspect extracted data first):

```powershell
# Step 1: Extract data
python cli.py extract --pdf-dir "C:\Users\HP\Desktop\test_invoices" --output "extracted.json"

# Step 2: Validate extracted data
python cli.py validate-cmd --input "extracted.json" --report "validation_report.json"
```

---

## Understanding the Output

### Terminal Output:
```
============================================================
FINAL RESULTS
============================================================
Total Invoices:  5
Valid:           3 ✓
Invalid:         2 ✗

TOP ISSUES:
  • invoice_number: Invoice number is missing: 2
  • invoice_date: Invoice date is missing: 1
  • gross_total: Totals mismatch: 1

✓ Detailed report saved to: validation_report.json
============================================================
```

### JSON Report Structure:
```json
{
  "total_invoices": 5,
  "valid_invoices": 3,
  "invalid_invoices": 2,
  "error_summary": {
    "invoice_number: Invoice number is missing": 2,
    "invoice_date: Invoice date is missing": 1
  },
  "detailed_results": [
    {
      "invoice_number": "INV-001",
      "is_valid": true,
      "errors": [],
      "warnings": []
    },
    {
      "invoice_number": "UNKNOWN",
      "is_valid": false,
      "errors": [
        {
          "field": "invoice_number",
          "message": "Invoice number is missing",
          "severity": "error"
        }
      ],
      "warnings": []
    }
  ]
}
```

---

## Command Options

### `full-run` command:
- `--pdf-dir` (required): Directory containing PDF invoices
- `--report` (optional): Output report filename (default: `validation_report.json`)

### `extract` command:
- `--pdf-dir` (required): Directory containing PDF invoices
- `--output` (optional): Output JSON filename (default: `extracted_invoices.json`)

### `validate-cmd` command:
- `--input` (required): Input JSON file with extracted invoices
- `--report` (optional): Output report filename (default: `validation_report.json`)

---

## Tips

1. **Use `full-run` for quick validation** - It's the fastest way to get results
2. **Use `extract` + `validate-cmd`** if you want to inspect extracted data before validation
3. **Check the JSON report** for detailed error information per invoice
4. **The CLI returns exit code 0** if all invoices are valid, **1** if any are invalid (useful for scripts)

---

## Troubleshooting

### "No PDF files found"
- Make sure the `--pdf-dir` path is correct
- Ensure the directory contains `.pdf` files

### "ModuleNotFoundError"
- Make sure you're in the `backend` directory
- Ensure the virtual environment is activated: `venv\Scripts\activate`

### "File not found" errors
- Use absolute paths or paths relative to the `backend` directory
- On Windows, use double quotes around paths with spaces

