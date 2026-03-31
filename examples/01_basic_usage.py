"""
Example 1: Basic Usage

This example shows the simplest way to use the OCR processor.
"""

from ai_ocr_gml_ocr import process_file

# Process a single file
result = process_file("input_pdf/document.pdf")

# Get all text
print(result.get_all_text())

# Get text from specific page
page_1_text = result.get_page_text(1)
print(f"Page 1: {page_1_text}")

# Save locations
print(f"TXT output: {result.txt_output}")
print(f"MD output: {result.md_output}")
