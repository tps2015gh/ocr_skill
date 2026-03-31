# Advanced OCR: Layout & Handwriting Support

This guide shows how to **extend OCR Skill** to support **complex layouts** and **handwritten text**.

> **⚠️ Important:** OCR Skill uses **Tesseract OCR by default**. This guide shows optional add-ons for advanced features.

---

## 🎯 Current Limitations (Tesseract OCR)

**Default Engine (Tesseract):**
- ❌ Poor with complex layouts (tables, forms, multi-column)
- ❌ Cannot recognize handwritten text
- ❌ Loses structure information
- ✅ Fast and free
- ✅ Good for printed Thai/English

---

## 📊 Quick Comparison

| Feature | Default (Tesseract) | With PaddleOCR Add-on | Cloud APIs |
|---------|---------------------|-----------------------|------------|
| **Layout** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Handwriting** | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Thai** | ✅ | ✅ | ✅ |
| **Cost** | Free | Free | Paid |
| **Speed** | Fast | Fast | Medium |
| **Setup** | Easy | Medium | Easy |

**Default Installation:** Tesseract OCR only (sufficient for most printed documents)

**Add PaddleOCR When:** You need handwriting recognition or complex layout preservation

---

## 📦 Installation Options

### Option A: Default (Tesseract Only) - Already Installed ✅

```bash
# This is what you have now - sufficient for printed documents
pip install pymupdf pytesseract pillow
```

### Option B: Add PaddleOCR (For Advanced Features)

```bash
# Add handwriting and layout support
pip install paddlepaddle paddleocr opencv-python
```

### Option C: Cloud APIs (Best Accuracy, Paid)

```bash
# Azure Form Recognizer
pip install azure-ai-formrecognizer

# Google Cloud Vision
pip install google-cloud-vision
```

---

## ✅ Solution 1: Add PaddleOCR (Recommended - Free)

PaddleOCR supports:
- ✅ Complex layout analysis
- ✅ Handwritten text recognition
- ✅ Thai language support
- ✅ Table detection
- ✅ Free and open-source

### Installation

```bash
pip install paddlepaddle paddleocr
```

### Usage

```python
# ocr_advanced.py
from paddleocr import PaddleOCR
import cv2

# Initialize with layout and handwriting support
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='th',  # Thai support
    det=True,   # Text detection
    rec=True,   # Text recognition
    cls=True,   # Layout classification
)

# Process document
image_path = "document.jpg"
result = ocr.ocr(image_path, cls=True)

# Extract with layout info
for line in result:
    if line:
        bbox = line[0][0]  # Bounding box
        text = line[1][0]  # Recognized text
        confidence = line[1][1]
        print(f"Text: {text} (Confidence: {confidence:.2f})")
```

### Integration with OCR Skill

```python
# ocr_skill/advanced.py
from paddleocr import PaddleOCR
from .skill import OCRSkill

class AdvancedOCR(OCRSkill):
    """OCR Skill with layout and handwriting support"""
    
    def __init__(self, languages='tha+eng', use_paddle=False):
        super().__init__(languages)
        self.use_paddle = use_paddle
        
        if use_paddle:
            self.paddle_ocr = PaddleOCR(
                use_angle_cls=True,
                lang='th',
                det=True,
                rec=True,
                cls=True,
            )
    
    def process_with_layout(self, file_path):
        """Process document preserving layout structure"""
        if not self.use_paddle:
            raise RuntimeError("PaddleOCR not enabled")
        
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        
        pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap()
            
            # Save temp image
            temp_path = f"temp_page_{page_num}.png"
            pix.save(temp_path)
            
            # OCR with layout
            result = self.paddle_ocr.ocr(temp_path, cls=True)
            
            # Extract structured data
            page_data = {
                'page': page_num + 1,
                'blocks': []
            }
            
            if result and result[0]:
                for line in result[0]:
                    bbox = line[0]
                    text = line[1][0]
                    confidence = line[1][1]
                    
                    page_data['blocks'].append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox,
                        'type': self._detect_block_type(bbox, text)
                    })
            
            pages.append(page_data)
        
        doc.close()
        return pages
    
    def _detect_block_type(self, bbox, text):
        """Detect if text is title, paragraph, table, etc."""
        # Simple heuristic based on position and length
        x, y = bbox[0], bbox[1]
        width = bbox[2] - bbox[0]
        
        if y < 100 and width > 200:
            return 'title'
        elif len(text) > 100:
            return 'paragraph'
        elif '|' in text or '\t' in text:
            return 'table'
        else:
            return 'text'
    
    def extract_handwriting(self, file_path):
        """Extract handwritten text"""
        if not self.use_paddle:
            raise RuntimeError("PaddleOCR required for handwriting")
        
        # PaddleOCR has better handwriting support than Tesseract
        result = self.paddle_ocr.ocr(file_path, cls=True)
        
        handwriting_blocks = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                
                # Lower confidence often indicates handwriting
                if confidence < 0.8:
                    handwriting_blocks.append({
                        'text': text,
                        'confidence': confidence,
                        'likely_handwriting': True
                    })
        
        return handwriting_blocks
```

### Usage Example

```python
from ocr_skill.advanced import AdvancedOCR

# Enable PaddleOCR for layout and handwriting
ocr = AdvancedOCR(use_paddle=True)

# Process with layout preservation
pages = ocr.process_with_layout("document.pdf")

for page in pages:
    print(f"\n=== Page {page['page']} ===")
    for block in page['blocks']:
        print(f"[{block['type']}] {block['text']}")

# Extract handwriting
handwriting = ocr.extract_handwriting("handwritten_note.jpg")
for item in handwriting:
    print(f"Handwritten: {item['text']} (Confidence: {item['confidence']:.2f})")
```

---

## ✅ Solution 2: Cloud APIs (Best Accuracy)

### Microsoft Azure Form Recognizer

Best for: Forms, tables, complex layouts

```python
# azure_ocr.py
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class AzureOCR:
    """Azure Form Recognizer for complex layouts"""
    
    def __init__(self, endpoint, key):
        self.client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
    
    def analyze_document(self, file_path, model_id="prebuilt-layout"):
        """Analyze document with layout preservation"""
        with open(file_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                model_id,
                f
            )
        
        result = poller.result()
        
        # Extract tables
        tables = []
        for table in result.tables:
            table_data = {
                'row_count': table.row_count,
                'column_count': table.column_count,
                'cells': []
            }
            
            for cell in table.cells:
                table_data['cells'].append({
                    'row': cell.row_index,
                    'col': cell.column_index,
                    'text': cell.content,
                    'is_header': cell.kind == 'columnHeader'
                })
            
            tables.append(table_data)
        
        # Extract paragraphs
        paragraphs = []
        for para in result.paragraphs:
            paragraphs.append({
                'text': para.content,
                'role': para.role  # title, sectionHeading, paragraph, etc.
            })
        
        return {
            'tables': tables,
            'paragraphs': paragraphs,
            'pages': result.pages
        }

# Usage
azure = AzureOCR(
    endpoint="https://your-resource.cognitiveservices.azure.com/",
    key="YOUR_API_KEY"
)

result = azure.analyze_document("complex_form.pdf")
print(f"Found {len(result['tables'])} tables")
print(f"Found {len(result['paragraphs'])} paragraphs")
```

### Google Cloud Vision API

Best for: Handwriting, multi-language

```python
# google_ocr.py
from google.cloud import vision

class GoogleOCR:
    """Google Cloud Vision for handwriting support"""
    
    def __init__(self, credentials_path):
        self.client = vision.ImageAnnotatorClient.from_service_account_json(
            credentials_path
        )
    
    def detect_handwriting(self, image_path):
        """Detect handwritten text"""
        with open(image_path, 'rb') as f:
            content = f.read()
        
        image = vision.Image(content=content)
        
        # Use TEXT_DETECTION with handwriting hint
        response = self.client.document_text_detection(
            image=image,
            image_context={'language_hints': ['th', 'en']}
        )
        
        texts = []
        for text_annotation in response.text_annotations:
            texts.append({
                'text': text_annotation.description,
                'bounding_box': text_annotation.bounding_poly.vertices
            })
        
        return texts[0] if texts else None
    
    def detect_fulltext(self, image_path):
        """Full text detection including handwriting"""
        with open(image_path, 'rb') as f:
            content = f.read()
        
        image = vision.Image(content=content)
        
        response = self.client.document_text_detection(
            image=image,
            image_context={'language_hints': ['th', 'en']}
        )
        
        # Extract structured text
        pages = []
        for page in response.full_text_annotation.pages:
            page_data = {
                'blocks': [],
                'confidence': page.confidence
            }
            
            for block in page.blocks:
                block_text = ''.join(
                    paragraph.symbols[0].text
                    for paragraph in block.paragraphs
                )
                
                page_data['blocks'].append({
                    'text': block_text,
                    'type': block.block_type.name
                })
            
            pages.append(page_data)
        
        return pages

# Usage
google = GoogleOCR("credentials.json")
result = google.detect_handwriting("handwritten_note.jpg")
print(f"Text: {result['text']}")
```

---

## ✅ Solution 3: Table Detection (LayoutPreservingOCR)

```python
# table_ocr.py
import cv2
import numpy as np
from ocr_skill import OCRSkill

class TableOCR(OCRSkill):
    """OCR with table structure preservation"""
    
    def detect_tables(self, image_path):
        """Detect table regions in image"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Find horizontal lines
        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (40, 1)
        )
        horizontal = cv2.morphologyEx(
            edges, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
        )
        
        # Find vertical lines
        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, 40)
        )
        vertical = cv2.morphologyEx(
            edges, cv2.MORPH_OPEN, vertical_kernel, iterations=2
        )
        
        # Combine lines
        table_mask = cv2.addWeighted(horizontal, 0.5, vertical, 0.5, 0)
        _, table_mask = cv2.threshold(table_mask, 10, 255, cv2.THRESH_BINARY)
        
        # Find contours (table regions)
        contours, _ = cv2.findContours(
            table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        tables = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100 and h > 50:  # Minimum table size
                tables.append({
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h
                })
        
        return tables
    
    def extract_table(self, image_path, table_region):
        """Extract table content as structured data"""
        import fitz
        
        # Crop table region
        doc = fitz.open(image_path)
        page = doc[0]
        
        # Extract text from table region
        rect = fitz.Rect(
            table_region['x'],
            table_region['y'],
            table_region['x'] + table_region['width'],
            table_region['y'] + table_region['height']
        )
        
        text = page.get_text("text", clip=rect)
        
        # Parse into rows/columns
        rows = text.strip().split('\n')
        table_data = []
        
        for row in rows:
            # Split by common delimiters
            cells = [cell.strip() for cell in row.split('|')]
            if len(cells) > 1:
                table_data.append(cells)
        
        doc.close()
        return table_data

# Usage
table_ocr = TableOCR()
tables = table_ocr.detect_tables("document.pdf")

for i, table in enumerate(tables):
    print(f"\nTable {i+1}:")
    data = table_ocr.extract_table("document.pdf", table)
    for row in data:
        print(" | ".join(row))
```

---

## 📊 Comparison

| Solution | Layout | Handwriting | Thai | Cost | Speed | Included |
|----------|--------|-------------|------|------|-------|----------|
| **Tesseract** | ⭐⭐ | ❌ | ✅ | Free | Fast | ✅ Yes (Default) |
| **PaddleOCR** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | Free | Fast | ❌ Optional |
| **Azure Form** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Paid | Medium | ❌ Optional |
| **Google Vision** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | Paid | Medium | ❌ Optional |
| **Table Detection** | ⭐⭐⭐⭐ | ❌ | ✅ | Free | Fast | ❌ Optional |

---

## 🚀 Recommended Setup

### For Best Results (Free):

```python
# hybrid_ocr.py
from ocr_skill import OCRSkill
from paddleocr import PaddleOCR

class HybridOCR:
    """Combine Tesseract + PaddleOCR for best results"""
    
    def __init__(self):
        self.tesseract = OCRSkill()  # For printed text
        self.paddle = PaddleOCR(
            use_angle_cls=True,
            lang='th',
            det=True,
            rec=True,
            cls=True,
        )  # For layout + handwriting
    
    def process(self, file_path, detect_handwriting=False):
        """Smart OCR that chooses best engine"""
        # First try PaddleOCR for layout
        paddle_result = self.paddle.ocr(file_path, cls=True)
        
        # Check if handwriting detected
        has_handwriting = False
        if paddle_result and paddle_result[0]:
            for line in paddle_result[0]:
                if line[1][1] < 0.8:  # Low confidence = possible handwriting
                    has_handwriting = True
                    break
        
        if has_handwriting and detect_handwriting:
            # Use PaddleOCR result
            return self._format_paddle_result(paddle_result)
        else:
            # Use Tesseract for better Thai accuracy
            return self.tesseract.extract_text(file_path)
    
    def _format_paddle_result(self, result):
        """Format PaddleOCR result"""
        text_blocks = []
        if result and result[0]:
            for line in result[0]:
                text_blocks.append({
                    'text': line[1][0],
                    'confidence': line[1][1],
                    'bbox': line[0][0]
                })
        return text_blocks

# Usage
ocr = HybridOCR()
result = ocr.process("mixed_document.pdf", detect_handwriting=True)
```

---

## 📦 Requirements

Add to `requirements.txt`:

```txt
# Current
pymupdf>=1.24.0
pytesseract>=0.3.10
pillow>=9.0.0

# For layout and handwriting support
paddlepaddle>=2.5.0
paddleocr>=2.7.0
opencv-python>=4.8.0

# Optional: Cloud APIs
azure-ai-formrecognizer>=3.3.0
google-cloud-vision>=3.4.0
```

---

## ⚠️ Important Notes

1. **PaddleOCR** requires more disk space (~500MB for models)
2. **Cloud APIs** require API keys and have usage costs
3. **Handwriting accuracy** varies by handwriting style
4. **Thai handwriting** is more challenging than printed Thai
5. **Processing time** increases with layout analysis

---

**Last Updated:** March 31, 2026
