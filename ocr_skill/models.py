"""
Data models for OCR results
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime
from pathlib import Path


@dataclass
class PageResult:
    """Result for a single page OCR"""
    page_number: int
    text: str
    confidence: float = 1.0


@dataclass
class OCRResult:
    """Result container for OCR processing"""
    file_path: str
    file_type: str
    total_pages: int
    processed_at: str
    pages: List[PageResult] = field(default_factory=list)
    txt_output: str = ''
    md_output: str = ''
    
    def get_all_text(self) -> str:
        """Get all text content as a single string"""
        return '\n\n'.join(page.text for page in self.pages)
    
    def get_page_text(self, page_num: int) -> str:
        """Get text for a specific page"""
        for page in self.pages:
            if page.page_number == page_num:
                return page.text
        return ''
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'file_path': self.file_path,
            'file_type': self.file_type,
            'total_pages': self.total_pages,
            'processed_at': self.processed_at,
            'pages': [
                {'page_number': p.page_number, 'text': p.text}
                for p in self.pages
            ],
            'txt_output': self.txt_output,
            'md_output': self.md_output
        }
    
    def save_txt(self, output_path: str) -> str:
        """Save result to TXT file"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"Original File: {self.file_path}\n")
            f.write(f"Processed: {self.processed_at}\n")
            f.write("="*80 + "\n\n")
            
            for page in self.pages:
                f.write(f"{'='*80}\n")
                f.write(f"Page {page.page_number}\n")
                f.write(f"{'='*80}\n\n")
                f.write(page.text)
                f.write("\n\n")
        
        self.txt_output = str(path)
        return self.txt_output
    
    def save_md(self, output_path: str) -> str:
        """Save result to MD file"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# OCR Output: {Path(self.file_path).name}\n\n")
            f.write(f"**Processed:** {self.processed_at}\n\n")
            f.write(f"**Original File:** `{self.file_path}`\n\n")
            f.write("---\n\n")
            
            for page in self.pages:
                f.write(f"## Page {page.page_number}\n\n")
                f.write(f"```\n{page.text}\n```\n\n")
                f.write("---\n\n")
        
        self.md_output = str(path)
        return self.md_output
