#!/usr/bin/env python3
"""
Test script for fixed PDF generation with SGPA chart.
"""

import os
import sys
from reports.generate_pdf_fixed import generate_pdf_report

def main():
    """Generate a test PDF report with SGPA chart."""
    print("Generating test PDF report with SGPA chart...")
    
    # Generate report for a single student with charts enabled
    pdf_path = generate_pdf_report(["23A95A6102"], includeCharts=True)
    
    if pdf_path and os.path.exists(pdf_path):
        print(f"✅ PDF successfully generated at: {pdf_path}")
        print(f"   File size: {os.path.getsize(pdf_path) / 1024:.2f} KB")
        print("\nYou can now open this PDF to verify that the SGPA chart is displayed correctly.")
    else:
        print("❌ PDF generation failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())