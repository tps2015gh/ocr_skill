"""
Example 2: Custom Configuration

This example shows how to use custom settings for OCR processing.
"""

from ai_ocr_gml_ocr import OCRProcessor

# Create processor with custom settings
processor = OCRProcessor(
    languages='tha+eng',  # Thai + English
    dpi=200,              # Higher DPI for better quality
    txt_output_dir='my_output_txt',
    md_output_dir='my_output_md',
    show_progress=True    # Show progress bar
)

# Process a file
result = processor.process_file_simple("input_pdf/document.pdf")

# Get results
print(f"Total pages: {result.total_pages}")
print(f"File type: {result.file_type}")
print(f"\nFirst 500 characters:\n{result.get_all_text()[:500]}")
