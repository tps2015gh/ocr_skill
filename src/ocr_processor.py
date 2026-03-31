"""
AI OCR Processor for PDF files
Supports Thai and English languages
Uses PyMuPDF for PDF rendering and Tesseract OCR
"""

import os
import sys
import fitz  # PyMuPDF
import configparser
from pathlib import Path
from datetime import datetime


class OCRProcessor:
    """Process PDF files with OCR and output to TXT and MD formats"""
    
    def __init__(self, config_path='config/config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')
        
        self.languages = self.config.get('ocr', 'languages', fallback='tha+eng')
        self.dpi = self.config.getint('ocr', 'dpi', fallback=300)
        self.txt_output_dir = self.config.get('output', 'txt_output_dir', fallback='output_txt')
        self.md_output_dir = self.config.get('output', 'md_output_dir', fallback='output_md')
        self.process_top_files = self.config.getint('processing', 'process_top_files', fallback=3)
        self.show_progress = self.config.getboolean('processing', 'show_progress', fallback=True)
        
        # Create output directories
        Path(self.txt_output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.md_output_dir).mkdir(parents=True, exist_ok=True)
    
    def get_pdf_files(self, input_dir):
        """Get all PDF files from input directory sorted by size (largest first)"""
        input_path = Path(input_dir)
        pdf_files = []
        
        for pdf_file in input_path.glob('*.pdf'):
            file_size = pdf_file.stat().st_size
            pdf_files.append((pdf_file, file_size))
        
        # Sort by size (largest first)
        pdf_files.sort(key=lambda x: x[1], reverse=True)
        return pdf_files
    
    def pdf_to_images(self, pdf_path, dpi=None):
        """Convert PDF pages to images - one at a time for memory efficiency"""
        if dpi is None:
            dpi = self.dpi
            
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Create transformation matrix for DPI
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            from PIL import Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Free memory
            pix = None
            
            yield (page_num + 1, img)
        
        doc.close()
    
    def perform_ocr(self, image, lang=None):
        """Perform OCR on image using pytesseract"""
        try:
            import pytesseract
            if lang is None:
                lang = self.languages
            
            # Set Tesseract path for Windows
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            return f"[OCR Error: {str(e)}]"
    
    def process_pdf(self, pdf_path, output_basename):
        """Process a single PDF file and save outputs"""
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*60}")
        
        # Convert PDF to images and process one at a time
        print("Converting and processing PDF pages...")
        
        # Get total page count first
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        doc.close()
        
        print(f"Total pages: {total_pages}")
        
        # Process each page
        all_text_pages = []
        
        for page_num, image in self.pdf_to_images(pdf_path):
            if self.show_progress:
                progress = (page_num / total_pages) * 100
                print(f"Progress: [{page_num}/{total_pages}] ({progress:.1f}%) - Processing page {page_num}...")
            
            # Perform OCR
            text = self.perform_ocr(image)
            all_text_pages.append((page_num, text))
            
            # Free memory
            image = None
        
        # Save outputs
        self.save_outputs(all_text_pages, output_basename, pdf_path.name)
        
        return all_text_pages
    
    def save_outputs(self, pages, basename, original_filename):
        """Save processed pages to TXT and MD files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save TXT (all pages in one file)
        txt_filepath = Path(self.txt_output_dir) / f"{basename}.txt"
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Original File: {original_filename}\n")
            f.write(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for page_num, text in pages:
                f.write(f"{'='*80}\n")
                f.write(f"Page {page_num}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
                f.write("\n\n")
        
        print(f"Saved TXT: {txt_filepath}")
        
        # Save MD (all pages in one file with markdown formatting)
        md_filepath = Path(self.md_output_dir) / f"{basename}.md"
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# OCR Output: {original_filename}\n\n")
            f.write(f"**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Original File:** `{original_filename}`\n\n")
            f.write("---\n\n")
            
            for page_num, text in pages:
                f.write(f"## Page {page_num}\n\n")
                f.write(f"```\n{text}\n```\n\n")
                f.write("---\n\n")
        
        print(f"Saved MD: {md_filepath}")
    
    def process_all(self, input_dir='input_pdf'):
        """Process all PDF files in input directory"""
        print("="*60)
        print("AI OCR Processor - Thai & English")
        print("="*60)
        print(f"Input Directory: {input_dir}")
        print(f"Output TXT Directory: {self.txt_output_dir}")
        print(f"Output MD Directory: {self.md_output_dir}")
        print(f"Languages: {self.languages}")
        print("="*60)
        
        # Get PDF files sorted by size
        pdf_files = self.get_pdf_files(input_dir)
        
        if not pdf_files:
            print("No PDF files found in input directory!")
            return
        
        print(f"\nFound {len(pdf_files)} PDF file(s)")
        print(f"Will process top {self.process_top_files} largest file(s)")
        
        # Process top N largest files
        files_to_process = pdf_files[:self.process_top_files]
        
        for i, (pdf_path, file_size) in enumerate(files_to_process, 1):
            size_mb = file_size / (1024 * 1024)
            print(f"\n[{i}/{len(files_to_process)}] File: {pdf_path.name} ({size_mb:.2f} MB)")
            
            # Create output basename
            output_basename = pdf_path.stem
            
            # Process the PDF
            self.process_pdf(pdf_path, output_basename)
        
        print("\n" + "="*60)
        print("Processing Complete!")
        print("="*60)
        print(f"Output files saved to:")
        print(f"  - TXT: {Path(self.txt_output_dir).absolute()}")
        print(f"  - MD: {Path(self.md_output_dir).absolute()}")


def main():
    """Main entry point"""
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    # Initialize and run processor
    processor = OCRProcessor()
    processor.process_all()


if __name__ == '__main__':
    main()
