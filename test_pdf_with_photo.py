#!/usr/bin/env python3
"""
Test script for PDF generation with student photo.
"""

import os
import sys
from reports.generate_pdf_with_styles import generate_pdf_report

def main():
    """Generate test PDFs with student photo in different styles."""
    print("Generating test PDFs with student photo...")
    
    styles = ["classic", "modern", "minimal"]
    reg_no = "23A95A6102"
    
    for style in styles:
        print(f"\nGenerating {style} style PDF...")
        pdf_path = generate_pdf_report([reg_no], includeCharts=True, template_style=style)
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ {style.capitalize()} PDF successfully generated at: {pdf_path}")
            print(f"   File size: {os.path.getsize(pdf_path) / 1024:.2f} KB")
        else:
            print(f"❌ {style.capitalize()} PDF generation failed.")
            return 1
    
    print("\nAll PDFs generated successfully!")
    print("You can now open these PDFs to verify that the student photo is displayed correctly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())