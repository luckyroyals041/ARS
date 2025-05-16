#!/usr/bin/env python3
"""
Test script for PDF generation with styling.
"""

import os
import sys
from reports.generate_pdf import generate_pdf_report

def main():
    """Generate a test PDF report with styling."""
    print("Generating test PDF report...")
    
    # Generate report for a single student
    pdf_path = generate_pdf_report(["23A95A6102"], includeCharts=True)
    
    if pdf_path and os.path.exists(pdf_path):
        print(f"✅ PDF successfully generated at: {pdf_path}")
        print(f"   File size: {os.path.getsize(pdf_path) / 1024:.2f} KB")
        print("\nYou can now open this PDF to verify that styles are applied correctly.")
    else:
        print("❌ PDF generation failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())