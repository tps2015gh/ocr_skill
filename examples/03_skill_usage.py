"""
Example 3: Using OCR Skill

This example shows how to use the OCR Skill interface,
perfect for AI agent integration.
"""

from ai_ocr_gml_ocr.skill import OCRSkill

# Initialize the skill
ocr = OCRSkill(languages='tha+eng')

# Scan a document and get text
text = ocr.extract_text("input_pdf/document.pdf")
print("Extracted text:")
print(text)

# Scan and get full result object
result = ocr.scan("input_pdf/image.png")
print(f"\nPages: {result.total_pages}")
print(f"TXT saved to: {result.txt_output}")
print(f"MD saved to: {result.md_output}")

# Scan multiple files
files = ["file1.pdf", "file2.png", "file3.jpg"]
results = ocr.scan_batch(files)
for r in results:
    print(f"{r.file_path}: {r.total_pages} pages")
