import click
import json
import os
from pathlib import Path
from extractor import InvoiceExtractor
from validator import InvoiceValidator
from datetime import datetime

extractor = InvoiceExtractor()
validator = InvoiceValidator()

@click.group()
def cli():
    """Invoice QC Service CLI Tool."""
    pass

@cli.command()
@click.option('--pdf-dir', type=click.Path(exists=True), required=True, help='Directory containing PDF invoices')
@click.option('--output', type=click.Path(), default='extracted_invoices.json', help='Output JSON file')
def extract(pdf_dir, output):
    """Extract invoice data from PDFs."""
    click.echo(f"Extracting invoices from: {pdf_dir}")
    
    pdf_files = list(Path(pdf_dir).glob('*.pdf'))
    if not pdf_files:
        click.echo("No PDF files found in directory")
        return
    
    extracted_invoices = []
    for pdf_file in pdf_files:
        click.echo(f"  Extracting: {pdf_file.name}", err=False)
        data = extractor.extract(str(pdf_file))
        extracted_invoices.append(data)
    
    # Save to JSON
    with open(output, 'w') as f:
        json.dump(extracted_invoices, f, indent=2)
    
    click.echo(f"\n✓ Extracted {len(extracted_invoices)} invoices")
    click.echo(f"✓ Saved to: {output}")

@cli.command()
@click.option('--input', type=click.Path(exists=True), required=True, help='Input JSON file with extracted invoices')
@click.option('--report', type=click.Path(), default='validation_report.json', help='Output validation report')
def validate_cmd(input, report):
    """Validate extracted invoice data."""
    click.echo(f"Validating invoices from: {input}")
    
    with open(input, 'r') as f:
        invoices = json.load(f)
    
    click.echo(f"  Processing {len(invoices)} invoices...")
    validation_report = validator.validate(invoices)
    
    # Save report
    with open(report, 'w') as f:
        json.dump(validation_report.dict(), f, indent=2)
    
    # Print summary
    click.echo("\n" + "="*60)
    click.echo("VALIDATION SUMMARY")
    click.echo("="*60)
    click.echo(f"Total Invoices:  {validation_report.total_invoices}")
    click.echo(f"Valid:           {validation_report.valid_invoices} ✓")
    click.echo(f"Invalid:         {validation_report.invalid_invoices} ✗")
    
    if validation_report.error_summary:
        click.echo("\nTOP ERRORS:")
        for error, count in sorted(validation_report.error_summary.items(), key=lambda x: x[1], reverse=True)[:5]:
            click.echo(f"  • {error}: {count}")
    
    click.echo(f"\n✓ Report saved to: {report}")
    click.echo("="*60)

@cli.command()
@click.option('--pdf-dir', type=click.Path(exists=True), required=True, help='Directory with PDFs')
@click.option('--report', type=click.Path(), default='validation_report.json', help='Output report')
def full_run(pdf_dir, report):
    """Extract and validate invoices in one command."""
    click.echo("Starting full invoice QC pipeline...")
    click.echo("="*60)
    
    # Step 1: Extract
    pdf_files = list(Path(pdf_dir).glob('*.pdf'))
    if not pdf_files:
        click.echo("No PDF files found")
        return
    
    click.echo(f"\n[1/2] EXTRACTION - Processing {len(pdf_files)} PDFs")
    extracted_invoices = []
    for pdf_file in pdf_files:
        click.echo(f"      • {pdf_file.name}", err=False)
        data = extractor.extract(str(pdf_file))
        extracted_invoices.append(data)
    
    # Step 2: Validate
    click.echo(f"\n[2/2] VALIDATION - Running business rules")
    validation_report = validator.validate(extracted_invoices)
    
    # Save report
    with open(report, 'w') as f:
        json.dump(validation_report.dict(), f, indent=2)
    
    # Print summary
    click.echo("\n" + "="*60)
    click.echo("FINAL RESULTS")
    click.echo("="*60)
    click.echo(f"Total Invoices:  {validation_report.total_invoices}")
    click.echo(f"Valid:           {validation_report.valid_invoices} ✓")
    click.echo(f"Invalid:         {validation_report.invalid_invoices} ✗")
    
    if validation_report.error_summary:
        click.echo("\nTOP ISSUES:")
        for error, count in sorted(validation_report.error_summary.items(), key=lambda x: x[1], reverse=True)[:5]:
            click.echo(f"  • {error}: {count}")
    
    click.echo(f"\n✓ Detailed report saved to: {report}")
    click.echo("="*60)
    
    return 0 if validation_report.invalid_invoices == 0 else 1

if __name__ == '__main__':
    cli()
