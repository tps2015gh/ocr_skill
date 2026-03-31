# OCR Skill Deployment Guide

This guide shows you how to deploy and use the OCR Skill in other projects.

---

## 📦 What is OCR Skill?

OCR Skill is a reusable Python package that provides Thai and English OCR capabilities. It uses Tesseract OCR engine and supports PDF, JPG, PNG, BMP, TIFF, and GIF files.

---

## 🚀 Deployment Options

### Option 1: Install as Python Package (Recommended)

Best for: Using the skill across multiple projects

**Steps:**

1. **Navigate to the OCR Skill directory:**
   ```bash
   cd D:\dev\ai_ocr_GML_OCR
   ```

2. **Install as editable package:**
   ```bash
   pip install -e .
   ```

3. **Use in any Python project:**
   ```python
   from ocr_skill import process_file
   
   result = process_file("document.pdf")
   print(result.get_all_text())
   ```

**Advantages:**
- ✅ Import from anywhere in your system
- ✅ Easy updates (just pull changes and it's updated everywhere)
- ✅ Clean project structure
- ✅ Can publish to PyPI if needed

---

### Option 2: Copy Package to Your Project

Best for: Self-contained projects, version control

**Steps:**

1. **Copy the `ocr_skill` folder to your project:**
   ```bash
   # Windows
   xcopy /E /I ocr_skill C:\path\to\your\project\
   
   # Linux/Mac
   cp -r ocr_skill /path/to/your/project/
   ```

2. **Your project structure:**
   ```
   your_project/
   ├── ocr_skill/          # ← Copied package
   │   ├── __init__.py
   │   ├── skill.py
   │   └── models.py
   ├── src/
   ├── tests/
   └── requirements.txt
   ```

3. **Add dependencies to your requirements.txt:**
   ```
   pymupdf>=1.24.0
   pytesseract>=0.3.10
   pillow>=9.0.0
   ```

4. **Use in your code:**
   ```python
   from ocr_skill import OCRProcessor
   
   processor = OCRProcessor()
   result = processor.process_file_simple("doc.pdf")
   ```

**Advantages:**
- ✅ Self-contained (no external dependencies)
- ✅ Version control with your project
- ✅ Works offline
- ✅ Easy to customize for specific needs

---

### Option 3: Git Submodule

Best for: Keeping package updated while maintaining version control

**Steps:**

1. **Add as submodule:**
   ```bash
   cd your_project
   git submodule add https://github.com/yourusername/ocr_skill.git
   ```

2. **Initialize submodule:**
   ```bash
   git submodule update --init --recursive
   ```

3. **Use in your code:**
   ```python
   import sys
   sys.path.append('ocr_skill')
   
   from ocr_skill import process_file
   ```

**Advantages:**
- ✅ Track specific commit
- ✅ Easy to update
- ✅ Clean separation

---

## 📋 Usage Examples

### Basic Usage

```python
from ocr_skill import process_file

# Process a PDF
result = process_file("document.pdf")
print(f"Pages: {result.total_pages}")
print(f"Text: {result.get_all_text()}")
```

### Using OCR Skill Class

```python
from ocr_skill.skill import OCRSkill

# Initialize
ocr = OCRSkill(languages='tha+eng')

# Extract text
text = ocr.extract_text("document.pdf")

# Get detailed result
result = ocr.scan("image.png")
print(f"File type: {result.file_type}")
print(f"Output files: {result.txt_output}, {result.md_output}")
```

### Batch Processing

```python
from ocr_skill.skill import OCRSkill

ocr = OCRSkill()

# Process multiple files
files = ["doc1.pdf", "doc2.png", "doc3.jpg"]
results = ocr.scan_batch(files)

for r in results:
    print(f"{r.file_path}: {r.total_pages} pages")
```

### Custom Configuration

```python
from ocr_skill import OCRProcessor

processor = OCRProcessor(
    languages='eng',      # English only
    dpi=200,              # Higher quality
    txt_output_dir='output',
    show_progress=True
)

result = processor.process_file_simple("document.pdf")
```

---

## 🔧 Requirements

Make sure the target system has:

1. **Python 3.8+**
2. **Tesseract OCR** installed with language packs:
   ```bash
   # Windows (Chocolatey)
   choco install tesseract --add-package-parameters "/Langs=tha,eng"
   
   # Ubuntu/Debian
   sudo apt install tesseract-ocr tesseract-ocr-tha tesseract-ocr-eng
   
   # macOS (Homebrew)
   brew install tesseract tessdata
   ```

3. **Python dependencies:**
   ```bash
   pip install pymupdf pytesseract pillow
   ```

---

## 📁 Files to Deploy

### Minimal Deployment (Copy these files/folders):

```
ocr_skill/              # Main package
├── __init__.py
├── skill.py
└── models.py

src/                    # Core processor
├── __init__.py
└── ocr_processor.py

requirements.txt        # Dependencies
```

### Full Deployment (Everything):

```
ocr_skill_project/
├── ocr_skill/          # Package
├── src/                # Source
├── config/             # Configuration (optional)
├── examples/           # Examples (optional)
├── setup.py            # For pip install
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

---

## ✅ Testing After Deployment

Create a test script to verify installation:

```python
# test_ocr.py
from ocr_skill import process_file

try:
    result = process_file("test.pdf")
    print("✓ OCR Skill is working!")
    print(f"  Pages: {result.total_pages}")
    print(f"  Text length: {len(result.get_all_text())} characters")
except Exception as e:
    print(f"✗ Error: {e}")
```

Run the test:
```bash
python test_ocr.py
```

---

## 🐛 Troubleshooting

### Import Error: `ModuleNotFoundError: No module named 'ocr_skill'`

**Solution 1:** Install the package
```bash
pip install -e .
```

**Solution 2:** Add to Python path
```python
import sys
sys.path.append('/path/to/ocr_skill')
```

### Tesseract Not Found

**Error:** `TesseractNotFoundError: tesseract is not found`

**Solution:** Install Tesseract OCR
```bash
# Windows
choco install tesseract

# Linux
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```

### Language Not Available

**Error:** `TesseractError: data file not found`

**Solution:** Install language packs
```bash
# Thai
sudo apt install tesseract-ocr-tha

# English (usually included)
sudo apt install tesseract-ocr-eng
```

---

## 📝 License

This OCR Skill is provided as-is for educational and practical use.

---

## 🤝 Support

For issues or questions:
1. Check the main README.md
2. Review examples in `examples/` folder
3. Check Tesseract documentation for OCR-specific issues

---

**Version:** 1.0.0  
**Last Updated:** March 31, 2026
