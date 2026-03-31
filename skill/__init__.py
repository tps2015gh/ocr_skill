"""
OCR Skill Package
==================

Thai and English OCR processor.

Usage:
    from skill import process_file
    result = process_file("document.pdf")
    text = result.get_all_text()
"""

from .ocr_skill import OCRProcessor, OCRResult, process_file, process_directory

__all__ = ['OCRProcessor', 'OCRResult', 'process_file', 'process_directory']
__version__ = '1.0.0'
