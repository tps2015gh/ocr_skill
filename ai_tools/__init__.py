"""
AI Tools for OCR Skill Project
===============================

Tools for AI agents to improve OCR quality through PDCA cycles.

Usage:
    from ai_tools import PDCATools
    tools = PDCATools()
    
    # Apply Thai text fixes
    fixed = tools.apply_all_fixes(text)
    
    # Calculate quality
    quality = tools.calculate_quality(text)
    
    # Batch process PDFs
    results = tools.batch_process_files("input_pdf")
"""

from .dev_tools import PDCATools

__all__ = ['PDCATools']
__version__ = '1.0.0'
