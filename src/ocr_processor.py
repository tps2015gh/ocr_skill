"""
AI OCR Processor for PDF and Image files
Supports Thai and English languages
Uses PyMuPDF for PDF rendering and Tesseract OCR
Supports: PDF, JPG, JPEG, PNG, BMP, TIFF, GIF
"""

import os
import sys
import fitz  # PyMuPDF
import configparser
from pathlib import Path
from datetime import datetime
from PIL import Image


class OCRResult:
    """Result container for OCR processing (for skill compatibility)"""
    
    def __init__(self, file_path, file_type, total_pages, processed_at):
        self.file_path = file_path
        self.file_type = file_type
        self.total_pages = total_pages
        self.processed_at = processed_at
        self.pages = []  # List of (page_number, text) tuples
        self.txt_output = ''
        self.md_output = ''
    
    def add_page(self, page_number, text):
        """Add a page result"""
        self.pages.append((page_number, text))
    
    def get_all_text(self) -> str:
        """Get all text content as a single string"""
        return '\n\n'.join(text for _, text in self.pages)
    
    def get_page_text(self, page_num: int) -> str:
        """Get text for a specific page"""
        for num, text in self.pages:
            if num == page_num:
                return text
        return ''
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'file_path': self.file_path,
            'file_type': self.file_type,
            'total_pages': self.total_pages,
            'processed_at': self.processed_at,
            'pages': [{'page_number': n, 'text': t} for n, t in self.pages],
            'txt_output': self.txt_output,
            'md_output': self.md_output
        }


class OCRProcessor:
    """
    Process PDF and Image files with OCR and output to TXT and MD formats.
    
    This class can be used in two modes:
    1. Config file mode (default): Loads settings from config.ini
    2. Direct parameter mode: Pass parameters directly for easy integration
    
    Example:
        # Using config file
        processor = OCRProcessor('config/config.ini')
        processor.process_all('input_pdf')
        
        # Using direct parameters (for integration)
        processor = OCRProcessor(
            languages='tha+eng',
            dpi=150,
            txt_output_dir='output_txt',
            md_output_dir='output_md'
        )
        result = processor.process_file_simple('document.pdf')
    """

    # Supported image extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}

    def __init__(self, config_path=None, languages=None, dpi=None,
                 txt_output_dir=None, md_output_dir=None,
                 process_top_files=None, show_progress=None):
        """
        Initialize OCR Processor.
        
        Args:
            config_path: Path to config.ini (optional)
            languages: OCR languages e.g., 'tha+eng' (overrides config)
            dpi: Rendering DPI (overrides config)
            txt_output_dir: TXT output directory (overrides config)
            md_output_dir: MD output directory (overrides config)
            process_top_files: Number of files to process (overrides config)
            show_progress: Show progress bar (overrides config)
        """
        self.config = configparser.ConfigParser()
        
        if config_path and os.path.exists(config_path):
            self.config.read(config_path, encoding='utf-8')
        
        # Load from config or use defaults/overrides
        self.languages = languages or self.config.get('ocr', 'languages', fallback='tha+eng')
        self.dpi = dpi or self.config.getint('ocr', 'dpi', fallback=150)
        self.txt_output_dir = txt_output_dir or self.config.get('output', 'txt_output_dir', fallback='output_txt')
        self.md_output_dir = md_output_dir or self.config.get('output', 'md_output_dir', fallback='output_md')
        self.process_top_files = process_top_files if process_top_files is not None else self.config.getint('processing', 'process_top_files', fallback=3)
        self.show_progress = show_progress if show_progress is not None else self.config.getboolean('processing', 'show_progress', fallback=True)

        # Create output directories
        Path(self.txt_output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.md_output_dir).mkdir(parents=True, exist_ok=True)

    def get_all_files(self, input_dir):
        """Get all PDF and image files from input directory sorted by size (largest first)"""
        input_path = Path(input_dir)
        files = []

        # Get PDF files
        for pdf_file in input_path.glob('*.pdf'):
            file_size = pdf_file.stat().st_size
            files.append((pdf_file, file_size, 'pdf'))

        # Get image files
        for ext in self.IMAGE_EXTENSIONS:
            for img_file in input_path.glob(f'*{ext}'):
                file_size = img_file.stat().st_size
                files.append((img_file, file_size, 'image'))
            # Also check uppercase extensions
            for img_file in input_path.glob(f'*{ext.upper()}'):
                file_size = img_file.stat().st_size
                files.append((img_file, file_size, 'image'))

        # Sort by size (largest first)
        files.sort(key=lambda x: x[1], reverse=True)
        return files

    def pdf_to_images(self, pdf_path, dpi=None):
        """Convert PDF pages to images - one at a time for memory efficiency"""
        if dpi is None:
            dpi = self.dpi

        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc[page_num]
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pix = None  # Free memory

            yield (page_num + 1, img)

        doc.close()

    def image_to_pages(self, image_path):
        """Load image file as single page"""
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        yield (1, img)
        img.close()

    def perform_ocr(self, image, lang=None):
        """Perform OCR on image using pytesseract"""
        try:
            import pytesseract
            if lang is None:
                lang = self.languages

            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            return f"[OCR Error: {str(e)}]"

    def process_file_simple(self, file_path) -> OCRResult:
        """
        Process a single file and return OCRResult object.
        Simplified method for easy integration.
        
        Args:
            file_path: Path to file (PDF or image)
        
        Returns:
            OCRResult object with text content and metadata
        """
        file_path = Path(file_path)
        file_type = 'image' if file_path.suffix.lower() in self.IMAGE_EXTENSIONS else 'pdf'
        
        # Create result object
        processed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = OCRResult(str(file_path), file_type, 0, processed_at)
        
        # Process based on file type
        if file_type == 'pdf':
            doc = fitz.open(file_path)
            result.total_pages = len(doc)
            doc.close()
            
            for page_num, image in self.pdf_to_images(file_path):
                text = self.perform_ocr(image)
                result.add_page(page_num, text)
                image = None
        else:
            result.total_pages = 1
            for page_num, image in self.image_to_pages(file_path):
                text = self.perform_ocr(image)
                result.add_page(page_num, text)
                image = None
        
        # Save outputs
        self._save_result(result, file_path.name)
        
        return result

    def process_file(self, file_path, file_type, output_basename):
        """Process a single file (PDF or image) and save outputs (legacy method)"""
        if self.show_progress:
            print(f"\n{'='*60}")
            print(f"Processing: {file_path.name}")
            print(f"Type: {file_type.upper()}")
            print(f"{'='*60}")

        all_text_pages = []

        if file_type == 'pdf':
            if self.show_progress:
                print("Converting and processing PDF pages...")

            doc = fitz.open(file_path)
            total_pages = len(doc)
            doc.close()

            if self.show_progress:
                print(f"Total pages: {total_pages}")

            for page_num, image in self.pdf_to_images(file_path):
                if self.show_progress:
                    progress = (page_num / total_pages) * 100
                    print(f"Progress: [{page_num}/{total_pages}] ({progress:.1f}%) - Processing page {page_num}...")

                text = self.perform_ocr(image)
                all_text_pages.append((page_num, text))
                image = None

        elif file_type == 'image':
            if self.show_progress:
                print("Processing image...")

            for page_num, image in self.image_to_pages(file_path):
                if self.show_progress:
                    print(f"Processing page {page_num}...")

                text = self.perform_ocr(image)
                all_text_pages.append((page_num, text))
                image = None

        self.save_outputs(all_text_pages, output_basename, file_path.name)
        return all_text_pages

    def _save_result(self, result: OCRResult, original_filename: str):
        """Save OCRResult to TXT and MD files"""
        # Save TXT
        txt_filepath = Path(self.txt_output_dir) / f"{Path(original_filename).stem}.txt"
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Original File: {original_filename}\n")
            f.write(f"Processed: {result.processed_at}\n")
            f.write("="*80 + "\n\n")
            for page_num, text in result.pages:
                f.write(f"{'='*80}\n")
                f.write(f"Page {page_num}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
                f.write("\n\n")
        result.txt_output = str(txt_filepath)

        # Save MD
        md_filepath = Path(self.md_output_dir) / f"{Path(original_filename).stem}.md"
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# OCR Output: {original_filename}\n\n")
            f.write(f"**Processed:** {result.processed_at}\n\n")
            f.write(f"**Original File:** `{original_filename}`\n\n")
            f.write("---\n\n")
            for page_num, text in result.pages:
                f.write(f"## Page {page_num}\n\n")
                f.write(f"```\n{text}\n```\n\n")
                f.write("---\n\n")
        result.md_output = str(md_filepath)

    def save_outputs(self, pages, basename, original_filename):
        """Save processed pages to TXT and MD files (legacy method)"""
        # Create result and save
        result = OCRResult(original_filename, 'pdf', len(pages), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for page_num, text in pages:
            result.add_page(page_num, text)
        self._save_result(result, original_filename)

    def process_all(self, input_dir='input_pdf'):
        """Process all PDF and image files in input directory"""
        print("="*60)
        print("AI OCR Processor - Thai & English")
        print("Supported: PDF, JPG, JPEG, PNG, BMP, TIFF, GIF")
        print("="*60)
        print(f"Input Directory: {input_dir}")
        print(f"Output TXT Directory: {self.txt_output_dir}")
        print(f"Output MD Directory: {self.md_output_dir}")
        print(f"Languages: {self.languages}")
        print("="*60)

        all_files = self.get_all_files(input_dir)

        if not all_files:
            print("No PDF or image files found in input directory!")
            return

        print(f"\nFound {len(all_files)} file(s) (PDF + Images)")
        print(f"Will process top {self.process_top_files} largest file(s)")

        files_to_process = all_files[:self.process_top_files]

        for i, (file_path, file_size, file_type) in enumerate(files_to_process, 1):
            size_mb = file_size / (1024 * 1024)
            print(f"\n[{i}/{len(files_to_process)}] File: {file_path.name} ({size_mb:.2f} MB) [{file_type.upper()}]")
            output_basename = file_path.stem
            self.process_file(file_path, file_type, output_basename)

        print("\n" + "="*60)
        print("Processing Complete!")
        print("="*60)
        print(f"Output files saved to:")
        print(f"  - TXT: {Path(self.txt_output_dir).absolute()}")
        print(f"  - MD: {Path(self.md_output_dir).absolute()}")


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)

    processor = OCRProcessor()
    processor.process_all()


if __name__ == '__main__':
    main()
