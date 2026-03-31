"""
OCR Skill - Easy integration module for other projects

This module provides a simplified interface for using the OCR processor
as a skill in AI agent systems or other applications.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, List, Union

from .models import OCRResult, PageResult
from .ocr_processor import OCRProcessor as BaseOCRProcessor


class OCRSkill:
    """
    OCR Skill for easy integration with AI agents and other systems.
    
    This class provides a simplified, high-level interface for OCR operations
    that can be easily called from AI agents, APIs, or other applications.
    
    Example:
        from ai_ocr_gml_ocr.skill import OCRSkill
        
        # Initialize skill
        ocr = OCRSkill()
        
        # Process a file
        result = ocr.scan("document.pdf")
        print(result.get_all_text())
        
        # Process with custom settings
        result = ocr.scan("image.png", languages="eng", return_dict=True)
    """
    
    def __init__(self, languages: str = 'tha+eng', dpi: int = 150,
                 output_dir: Optional[str] = None):
        """
        Initialize OCR Skill.
        
        Args:
            languages: OCR languages (default: 'tha+eng')
            dpi: Rendering DPI (default: 150)
            output_dir: Output directory (default: creates in current dir)
        """
        self.languages = languages
        self.dpi = dpi
        self.output_dir = output_dir or 'output'
        
        # Create output directories
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}_txt").mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}_md").mkdir(parents=True, exist_ok=True)
    
    def scan(self, file_path: Union[str, Path], languages: Optional[str] = None,
             return_dict: bool = False) -> Union[OCRResult, dict]:
        """
        Scan a file with OCR and return the result.
        
        Args:
            file_path: Path to file (PDF, JPG, PNG, BMP, TIFF, GIF)
            languages: Override default languages
            return_dict: Return as dictionary instead of OCRResult
        
        Returns:
            OCRResult object or dictionary with OCR data
        """
        lang = languages or self.languages
        
        processor = BaseOCRProcessor(
            languages=lang,
            dpi=self.dpi,
            txt_output_dir=f"{self.output_dir}_txt",
            md_output_dir=f"{self.output_dir}_md",
            show_progress=False
        )
        
        result = processor.process_file_simple(str(file_path))
        
        if return_dict:
            return result.to_dict()
        return result
    
    def scan_batch(self, file_paths: List[Union[str, Path]], 
                   languages: Optional[str] = None) -> List[OCRResult]:
        """
        Scan multiple files with OCR.
        
        Args:
            file_paths: List of file paths
            languages: Override default languages
        
        Returns:
            List of OCRResult objects
        """
        results = []
        for file_path in file_paths:
            result = self.scan(file_path, languages)
            results.append(result)
        return results
    
    def extract_text(self, file_path: Union[str, Path], 
                     languages: Optional[str] = None) -> str:
        """
        Extract text from a file (convenience method).
        
        Args:
            file_path: Path to file
            languages: Override default languages
        
        Returns:
            All text content as a single string
        """
        result = self.scan(file_path, languages)
        return result.get_all_text()
    
    def extract_text_by_page(self, file_path: Union[str, Path],
                             languages: Optional[str] = None) -> List[str]:
        """
        Extract text from a file, separated by page.
        
        Args:
            file_path: Path to file
            languages: Override default languages
        
        Returns:
            List of text strings (one per page)
        """
        result = self.scan(file_path, languages)
        return [page.text for page in result.pages]


# Convenience function for quick usage
def ocr_scan(file_path: str, languages: str = 'tha+eng') -> str:
    """
    Quick OCR scan - returns all text content.
    
    Args:
        file_path: Path to file
        languages: OCR languages
    
    Returns:
        All text content as string
    """
    skill = OCRSkill(languages=languages)
    return skill.extract_text(file_path)
