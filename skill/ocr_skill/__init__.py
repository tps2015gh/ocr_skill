"""
OCR Skill - A reusable OCR skill for Thai and English documents

This package provides a simple, reusable OCR processor that can be easily
integrated into other projects or used as a standalone skill.

Usage:
    from ocr_skill import OCRProcessor, process_file, process_directory
    
    # Simple function usage
    result = process_file("document.pdf")
    
    # Class usage with custom config
    processor = OCRProcessor(languages="tha+eng", dpi=150)
    result = processor.process_file_simple("image.png")
    
    # Use as a skill
    from ocr_skill.skill import OCRSkill
    skill = OCRSkill()
    text = skill.extract_text("document.pdf")
"""

__version__ = '1.0.0'
__author__ = 'Qwen Code AI Assistant'
__description__ = 'OCR processor for Thai and English documents (PDF, JPG, PNG, BMP, TIFF)'

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from ocr_processor import OCRProcessor, OCRResult


# Convenience functions for easy integration
def process_file(file_path, output_dir=None, languages='tha+eng', dpi=150, show_progress=False):
    """
    Process a single file (PDF or image) with OCR.
    
    Args:
        file_path: Path to the file (PDF, JPG, PNG, BMP, TIFF, GIF)
        output_dir: Optional output directory (default: creates output_txt/output_md in current dir)
        languages: OCR languages (default: 'tha+eng' for Thai + English)
        dpi: Rendering DPI (default: 150)
        show_progress: Show progress bar (default: False)
    
    Returns:
        OCRResult object with text content and metadata
    """
    processor = OCRProcessor(
        languages=languages,
        dpi=dpi,
        txt_output_dir=output_dir or 'output_txt',
        md_output_dir='output_md' if output_dir is None else output_dir.replace('txt', 'md'),
        show_progress=show_progress
    )
    return processor.process_file_simple(file_path)


def process_directory(input_dir, output_dir=None, languages='tha+eng', dpi=150, 
                      process_count=3, show_progress=True):
    """
    Process multiple files from a directory.
    
    Args:
        input_dir: Directory containing files to process
        output_dir: Optional output directory
        languages: OCR languages (default: 'tha+eng')
        dpi: Rendering DPI (default: 150)
        process_count: Number of files to process (default: 3)
        show_progress: Show progress bar (default: True)
    
    Returns:
        List of OCRResult objects
    """
    processor = OCRProcessor(
        languages=languages,
        dpi=dpi,
        txt_output_dir=output_dir or 'output_txt',
        md_output_dir='output_md' if output_dir is None else output_dir.replace('txt', 'md'),
        process_top_files=process_count,
        show_progress=show_progress
    )
    return processor.process_all(input_dir)


# Export main classes and functions
__all__ = ['OCRProcessor', 'OCRResult', 'process_file', 'process_directory']
